from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from src.state_template import GraphState
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate


def generate(state: GraphState):
    """
    state: Graph of the state
  """
    question = state["question"]
    documents = state["documents"]
    retries = state["retries"] if state.get("retries") is not None else -1
    # prompt = hub.pull("rlm/rag-prompt")
    prompt = """ 
        Use the following information about Amazon Order Sales Report tasked with answering questions about sales.
        Your task is to generate answers. Follow these guidelines:
        1. **Base your answer only on the retrieved information**. Do not include information that is not found in the 
        context, and do not make assumptions beyond what is provided.
        2. If the context does not provide enough information to answer the question, say, again model can search and 
        get information about that.
        3. Keep your response **concise** and **relevant**. Ensure it is **fact-based** and helpful to the user's 
        orders needs.
        Retrieved Amazon Order Sales Report Information:
        {context}
        User Question:
        {question}
        
    """
    prompt = ChatPromptTemplate.from_template(prompt)
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")
    rag_chain = prompt | llm | StrOutputParser()
    return {"question": question, "documents": documents,
            "generation": rag_chain.invoke({"question": question, "context": documents}),
            "retires": retries + 1}
