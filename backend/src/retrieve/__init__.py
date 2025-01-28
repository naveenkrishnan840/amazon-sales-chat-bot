from qdrant_client import models, QdrantClient
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core import VectorStoreIndex

from backend.src.selfrag

client = QdrantClient(url="https://954bd036-8115-4593-b8be-59eb78baceb2.us-west-1-0.aws.cloud.qdrant.io",
                      api_key="31b9lK5UBtV0BUD36w9aDcEFb2ZmrTwH-pncdtEU7xLDqmcDWqjEXg")

amazon_datasets_store = QdrantVectorStore(collection_name="amazon_sales_datasets", client=client, enable_hybrid=True)
retriever = VectorStoreIndex.from_vector_store(amazon_datasets_store).as_retriever(
    similarity_top_k=5, alpha=0.5, sparse_top_k=0.5, hybrid_top_k=0.5)


def retrieve(state: GraphState) -> GraphState:
    """
    state: Graph of the state
  """
    question = state["question"]
    docs = retriever.retrieve(question)

    return {"question": question, "documents": docs, "generation": ""}
