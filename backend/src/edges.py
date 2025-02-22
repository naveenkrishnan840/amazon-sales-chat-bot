from src.state_template import GraphState, MAX_RETRIES
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import ensure_config
from langchain_core.prompts import ChatPromptTemplate

from src.structured_output import GradeAnswer, GradeHallucinations

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
    retries = state["retries"] if state.get("retries") else -1
    config = ensure_config()
    max_retries = config.get("configurable", {}).get("max_retries", MAX_RETRIES)
    if not web_fallback:
        return "generate"

    structured_llm_grader = ChatGoogleGenerativeAI(model="gemini-2.0-flash").with_structured_output(
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
        structured_llm_grader = ChatGoogleGenerativeAI(model="gemini-2.0-flash").with_structured_output(GradeAnswer)
        answer_grader = answer_prompt | structured_llm_grader
        grade = answer_grader.invoke({"question": question, "generation": generation})
        if grade.binary_score == "yes":
            return "end"
        else:
            return "transform_query" if retries < max_retries else "web_search"
    else:
        return "generate" if retries < max_retries else "web_search"

