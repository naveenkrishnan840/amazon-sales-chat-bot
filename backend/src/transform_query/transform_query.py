from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from src.state_template import GraphState


def transform_query(state: GraphState) -> GraphState:
    """
    state: Graph of the state
  """
    system = """You a question re-writer that converts an input question to a better version that is optimized \n 
     for vectorstore retrieval. Look at the input and try to reason about the underlying semantic intent / meaning."""
    re_write_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            (
                "human",
                "Here is the initial question: \n\n {question} \n Formulate an improved question.",
            ),
        ]
    )

    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")
    question = state["question"]
    documents = state["documents"]
    rewriter_llm = re_write_prompt | llm | StrOutputParser()

    return {"question": rewriter_llm.invoke({"question": question}), "generation": "", "documents": documents}
