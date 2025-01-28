from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from src.state_template import GraphState
from langchain_google_genai import ChatGoogleGenerativeAI


def generate(state: GraphState) -> GraphState:
    """
    state: Graph of the state
  """
    question = state["question"]
    documents = state["documents"]
    retries = state["retries"] if state.get("retries") is not None else -1
    prompt = hub.pull("rlm/rag-prompt")
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")
    rag_chain = prompt | llm | StrOutputParser()
    return {"question": question, "documents": documents,
            "generation": rag_chain.invoke({"question": question, "context": documents}),
            "retires": retries + 1}
