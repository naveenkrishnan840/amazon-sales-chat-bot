from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI

from src.state_template import GraphState
from src.structured_output import GradeDocuments

# Prompt
system = """You are a grader assessing relevance of a retrieved document to a user question. \n 
    It does not need to be a stringent test. The goal is to filter out erroneous retrievals. \n
    If the document contains keyword(s) or semantic meaning related to the user question, grade it as relevant. \n
    Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question."""
grade_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "Retrieved document: \n\n {document} \n\n User question: {question}"),
    ]
)


llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")
structured_llm_grader = llm.with_structured_output(schema=GradeDocuments)
retrieval_grader = grade_prompt | structured_llm_grader


def grade_documents(state: GraphState) -> GraphState:
    """
    state: Graph of the state
  """
    question = state["question"]
    documents = state["documents"]

    filtered_docs = []
    for doc in documents:
        grade = retrieval_grader.invoke({"document": doc.text, "question": question})
        if grade.binary_score == "yes":
            filtered_docs.append(doc)
    return {"question": question, "documents": filtered_docs, "generation": ""}
