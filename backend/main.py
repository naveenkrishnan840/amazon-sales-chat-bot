from langgraph.graph import StateGraph, START, END
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import ensure_config
from fastapi import FastAPI, APIRouter, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
import uuid


from src.state_template import GraphState, MAX_RETRIES, GraphConfig
from src.retrieve.retrieve import retrieve
from src.search_tool.web_search_tool import web_search
from src.grade_documents.grade_document import grade_documents
from src.transform_query.transform_query import transform_query
from src.generate.generate import generate
from src.structured_output import GradeAnswer, GradeHallucinations

# import os
# os.environ["GROQ_API_KEY"] = "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"

app = FastAPI(name="Amazon Sales Report using Self Corrective RAG")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

api_router = APIRouter()

self_rag_workflow = StateGraph(GraphState, config_schema=GraphConfig)
self_rag_workflow.add_node("retrieve", retrieve)
self_rag_workflow.add_node("grade_documents", grade_documents)
self_rag_workflow.add_node("transform_query", transform_query)
self_rag_workflow.add_node("generate", generate)
self_rag_workflow.add_node("web_search_tool", web_search)
self_rag_workflow.add_edge(start_key=START, end_key="retrieve")
self_rag_workflow.add_edge(start_key="retrieve", end_key="grade_documents")
self_rag_workflow.add_edge(start_key="web_search_tool", end_key="generate")


def decide_to_generate(state: GraphState) -> str:
    """
    state: Graph of the state
  """
    question = state["question"]
    filtered_docs = state["documents"]
    if not filtered_docs:
        return "transform_query"
    else:
        return "generate"


def grade_generation_generation_question(state: GraphState) -> str:
    """
    state: Graph of the state
  """
    documents = state["documents"]
    question = state["question"]
    generation = state["generation"]
    web_fallback = state["web_fallback"]
    retries = state["retries"] if state.get("retries") is not None else -1
    config = ensure_config()
    max_retries = config.get("configurable", {}).get("max_retries", MAX_RETRIES)
    if not web_fallback:
        return "generate"

    structured_llm_grader = ChatGoogleGenerativeAI(model="gemini-1.5-pro").with_structured_output(
        schema=GradeHallucinations)

    system = """You are a grader assessing whether an LLM generation is grounded in / supported by a set of retrieved facts. \n 
      Give a binary score 'yes' or 'no'. 'Yes' means that the answer is grounded in / supported by the set of facts."""
    hallucination_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("human", "Set of facts: \n\n {documents} \n\n LLM generation: {generation}"),
        ]
    )
    hallucinations_grader = hallucination_prompt | structured_llm_grader
    score = hallucinations_grader.invoke({"documents": documents, "generation": generation})
    if score.binary_score == "yes":
        system = """You are a grader assessing whether an answer addresses / resolves a question \n 
     Give a binary score 'yes' or 'no'. Yes' means that the answer resolves the question."""
        answer_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system),
                ("human", "User question: \n\n {question} \n\n LLM generation: {generation}"),
            ]
        )
        structured_llm_grader = ChatGoogleGenerativeAI(model="gemini-1.5-pro").with_structured_output(GradeAnswer)
        answer_grader = answer_prompt | structured_llm_grader
        grade = answer_grader.invoke({"question": question, "generation": generation})
        if grade.binary_score == "yes":
            return "end"
        else:
            return "transform_query" if retries < max_retries else "web_search"
    else:
        return "generate_answer" if retries < max_retries else "web_search"


self_rag_workflow.add_conditional_edges(source="grade_documents", path=decide_to_generate,
                                        path_map={"generate": "generate", "transform_query": "transform_query"})
self_rag_workflow.add_edge(start_key="transform_query", end_key="retrieve")
self_rag_workflow.add_conditional_edges(source="generate", path=grade_generation_generation_question,
                                        path_map={"end": END, "generate": "generate",
                                                  "transform_query": "transform_query"})

memory = MemorySaver()
CRAG_compiled_graph = self_rag_workflow.compile(
    checkpointer=memory,
)

config = {
    "configurable": {
        "thread_id": uuid.uuid4()
    }
}



@api_router.post("/bot-message-request")
async def bot_message_request(request: Request, chat_bot_input: BotRequest):

    stream = CRAG_compiled_graph.stream(input={"question": chat_bot_input.input_msg.strip()}, config=config, stream_mode="updates")

    generation_response = [st for st in stream]
    result = generation_response[-1]["generate"]["generation"]

    return HTTPException(
        status_code=200,
        detail=result
    )

app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app=app, host="0.0.0.0", port=8004)

