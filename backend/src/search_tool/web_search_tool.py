from langchain_core.tools import tool
from langchain_core.documents import Document
from langchain_community.tools.tavily_search import TavilySearchResults

from src.state_template import GraphState


def web_search(state: GraphState):
    """Returns Question & documents based on Tavily Search"""
    question = state["question"]
    documents = state["documents"]
    tavily_search_tool = TavilySearchResults(max_results=3, include_answer=True, include_raw_content=True,
                                             include_images=True)
    docs = tavily_search_tool.invoke(input=question)

    content = "\n".join([doc["content"] for doc in docs])
    documents.append(Document(page_content=content))

    return {"question": question, "documents": documents, "web_fallback": False}

