from langgraph.graph import StateGraph, START, END
from functools import lru_cache
from llama_index.core import Settings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from llama_index.embeddings.langchain import LangchainEmbedding
from dotenv import load_dotenv

from src.state_template import GraphState, MAX_RETRIES, GraphConfig
from src.retrieve.retrieve import retrieve
from src.search_tool.web_search_tool import web_search
from src.grade_documents.grade_document import grade_documents
from src.transform_query.transform_query import transform_query
from src.generate.generate import generate
from src.structured_output import GradeAnswer, GradeHallucinations
from src.edges import decide_to_generate, grade_generation_generation_question


load_dotenv()
Settings.embed_model = LangchainEmbedding(GoogleGenerativeAIEmbeddings(model="models/embedding-001"))


@lru_cache(maxsize=1)
def create_workflow():
    self_rag_workflow = StateGraph(GraphState, config_schema=GraphConfig)
    self_rag_workflow.add_node("retriever", retrieve)
    self_rag_workflow.add_node("grade_documents", grade_documents)
    self_rag_workflow.add_node("transform_query", transform_query)
    self_rag_workflow.add_node("generate", generate)
    self_rag_workflow.add_node("web_search_tool", web_search)
    self_rag_workflow.add_edge(start_key=START, end_key="retriever")
    self_rag_workflow.add_edge(start_key="retriever", end_key="grade_documents")
    self_rag_workflow.add_edge(start_key="web_search_tool", end_key="generate")
    self_rag_workflow.add_conditional_edges(source="grade_documents", path=decide_to_generate,
                                            path_map={"generate": "generate", "transform_query": "transform_query"})
    self_rag_workflow.add_edge(start_key="transform_query", end_key="retriever")
    self_rag_workflow.add_conditional_edges(source="generate", path=grade_generation_generation_question,
                                            path_map={"end": END, "generate": "generate",
                                                      "transform_query": "transform_query",
                                                      "web_search": "web_search_tool"})

    return self_rag_workflow


graph = create_workflow().compile()