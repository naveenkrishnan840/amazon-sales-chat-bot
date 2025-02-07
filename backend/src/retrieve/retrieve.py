from qdrant_client import QdrantClient
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core import VectorStoreIndex
from src.state_template import GraphState

client = QdrantClient(url="localhost", port=6333)


def retrieve(state: GraphState):
    """
    state: Graph of the state
  """
    question = state["question"]
    amazon_datasets_store = QdrantVectorStore(collection_name="amazon_sales_datasets", client=client,
                                              enable_hybrid=True)
    retriever = VectorStoreIndex.from_vector_store(amazon_datasets_store).as_retriever(
        similarity_top_k=5, alpha=0.5, sparse_top_k=0.5, hybrid_top_k=0.5)
    docs = retriever.retrieve(question)

    return {"question": question, "documents": docs, "web_fallback": True}

