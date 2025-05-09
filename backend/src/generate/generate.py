from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import os

from src.state_template import GraphState


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
        4. Structure the answer using **HTML** tags such as '<div>', '<p>', '<ul>', '<li>', '<strong>', '<table>', 
        '<section>', '<code>', '<b>', '<hr>', '<ol>' and others as needed for clear, readable output.
        5. Use **CSS** inline styles or class attributes to style the content appropriately (e.g., font-size, margin, 
        padding, font-weight, border, overflow, border-style, font-bold, ).
        6. Keep the HTML clean and semantically correct. Avoid unnecessary tags or styles ot html tags, single quotes.
        7. If a question requires an explanation or list, format the content using '<ul>' or '<ol>' lists.
        Retrieved Amazon Order Sales Report Information:
        {context}
        User Question:
        {question}
        
    """
    prompt = ChatPromptTemplate.from_template(prompt)
    # llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")
    llm = (ChatOpenAI(base_url=os.getenv("OPENROUTER_BASE_URL"), model=os.getenv("MODEL_NAME")))

    rag_chain = prompt | llm | StrOutputParser()
    return {"question": question, "documents": documents,
            "generation": rag_chain.invoke({"question": question, "context": documents}),
            "retires": retries + 1}
