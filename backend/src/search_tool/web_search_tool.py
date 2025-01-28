from langchain_core.tools import tool
from langchain_core.documents import Document
from backend.src.graph_msg_templ import GraphState
from langchain_community.tools.tavily_search import TavilySearchResults

import os
os.environ["TAVILY_API_KEY"] = "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"
tavily_search_tool = TavilySearchResults(max_results=3, include_answer=True, include_raw_content=True,
                                         include_images=True)


# @tool
def web_search(state: GraphState):
    """Returns Question & documents based on Tavily Search"""
    question = state["question"]
    documents = state["documents"]
    docs = tavily_search_tool.invoke(input=question)

    content = "\n".join([doc["content"] for doc in docs])
    documents.append(Document(page_content=content))

    return {"question": question, "documents": documents, "web_fallback": False}

