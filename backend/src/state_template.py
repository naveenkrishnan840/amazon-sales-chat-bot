from langgraph.graph import StateGraph
from typing import List, TypedDict


class GraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        question: question
        generation: LLM generation
        documents: list of documents
  """
    generation: str
    question: str
    documents: List[str]
    retires: int
    web_fallback: bool


class GraphConfig(TypedDict):
    max_retries: int


MAX_RETRIES = 3

