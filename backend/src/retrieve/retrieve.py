import os

from qdrant_client import QdrantClient
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core import VectorStoreIndex
from llama_index.core.vector_stores.types import VectorStoreQueryMode

from src.state_template import GraphState


def retrieve(state: GraphState):
    """
    state: Graph of the state
  """
    question = state["question"]
    client = QdrantClient(url=os.getenv("QDRANT_URL"), api_key=os.getenv("QDRANT_API_KEY"))
    amazon_datasets_store = QdrantVectorStore(collection_name="amazon_sales_datasets", client=client,
                                              enable_hybrid=True)
    retriever = VectorStoreIndex.from_vector_store(amazon_datasets_store).as_retriever(
        vector_store_query_mode=VectorStoreQueryMode.HYBRID,
        similarity_top_k=5, alpha=0.7, sparse_top_k=10, hybrid_top_k=10)
    docs = retriever.retrieve(question)

    return {"question": question, "documents": docs, "web_fallback": True}

