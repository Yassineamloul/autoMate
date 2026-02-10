from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

class GradeDocuments(BaseModel):
    """Binary score for relevance check on retrieved documents."""
    binary_score: str = Field(description="Documents are relevant to the question, 'yes' or 'no'")


llm = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    temperature=1.0,
    thinking_level="low",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)
structured_llm_grader = llm.with_structured_output(GradeDocuments)

system = """You are a grader assessing relevance of a retrieved document to a user question.
If the document contains keyword(s) or semantic meaning related to the user question, grade it as relevant.
It does not need to be a stringent test. The goal is to filter out erroneous retrievals.
Return ONLY a JSON object exactly like {{"binary_score":"yes"}} or {{"binary_score":"no"}}..
No other text. 'Yes' means that the document is relevant to the question."""
grade_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "Retrieved document:\n\n{document}\n\nUser question: {question}"),
    ]
)

# ✅ Export utilisé par graph.py
retrieval_grader = grade_prompt | structured_llm_grader


if __name__ == "__main__":
    # ✅ Test local (ne s'exécute PAS quand graph.py importe ce fichier)
    from .index import retriever

    question = "agent memory"
    docs = retriever.invoke(question)
    doc_txt = docs[0].page_content if docs else ""
    print(retrieval_grader.invoke({"question": question, "document": doc_txt}))
