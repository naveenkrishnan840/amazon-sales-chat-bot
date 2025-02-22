from fastapi import FastAPI, APIRouter, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.stores import InMemoryStore
import uuid
from dotenv import load_dotenv
# from langchain_huggingface import HuggingFaceEmbeddings

from src.request_validate import QueryRequest
from src.build_graph import create_workflow

# import os
# os.environ["GROQ_API_KEY"] = "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"

app = FastAPI(name="Amazon Sales Report using Self Corrective RAG")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

api_router = APIRouter()

load_dotenv()
# model_name = "sentence-transformers/all-mpnet-base-v2"
# model_kwargs = {'device': 'cpu'}
# encode_kwargs = {'normalize_embeddings': False}
# hf = HuggingFaceEmbeddings(
#     model_name=model_name,
#     model_kwargs=model_kwargs,
#     encode_kwargs=encode_kwargs
# )
# Settings.embed_model = hf
# Settings.llm =
self_rag_workflow = create_workflow()

@api_router.post("/chatBotInitialize")
async def rendering_bot(request: Request):
    try:
        memory = MemorySaver()
        in_vector_store = InMemoryStore()
        self_rag_compiled_graph = self_rag_workflow.compile(
            checkpointer=memory, store=in_vector_store
        )
        request.app.workflow = self_rag_compiled_graph
        config = {
            "recursion_limit": 100,
            "configurable": {
                "thread_id": uuid.uuid4()
            }
        }
        request.app.graph_config = config

        return HTTPException(status_code=200, detail={})
    except Exception as e:
        raise e


async def streaming_response(query: str, self_rag_compiled_graph, graph_config):
    try:
        for event in self_rag_compiled_graph.stream(input={"question": query.strip()}, config=graph_config):
            try:
                if "generate" in event:
                    yield event.get("generate", "").get("generation", "")
            except Exception as e:
                raise e
    except Exception as e:
        raise e
    # generation_response = [st for st in stream]
    # result = generation_response[-1]["generate"]["generation"]


@api_router.post("/bot-message-request")
async def bot_message_request(request: Request, chat_bot_input: QueryRequest):
    self_rag_compiled_graph = request.app.workflow
    graph_config = request.app.graph_config
    return StreamingResponse(content=streaming_response(chat_bot_input.query.strip(), self_rag_compiled_graph,
                                                        graph_config),
                             media_type="text/event-stream")

app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app=app, host="127.0.0.1", port=8004)

