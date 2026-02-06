from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate

class GradeDocuments(BaseModel):
    binary_score: str = Field(description="Documents are relevant to the question, 'yes' or 'no'")

llm = ChatOllama(model="gpt-oss:120b-cloud", temperature=0.0, format="json")
structured_llm_grader = llm.with_structured_output(GradeDocuments)

system = """You are a grader assessing relevance of a retrieved document to a user question.
If the document contains keyword(s) or semantic meaning related to the user question, grade it as relevant.
It does not need to be a stringent test. The goal is to filter out erroneous retrievals.
Give a binary score 'yes' or 'no'.

You MUST respond with valid JSON in this exact format:
{{"binary_score": "yes"}} or {{"binary_score": "no"}}

Use the string values "yes" or "no", not numbers or other values."""

grade_prompt = ChatPromptTemplate.from_messages([
    ("system", system),
    ("human", "Retrieved document:\n\n{document}\n\nUser question: {question}"),
])

retrieval_grader = grade_prompt | structured_llm_grader

# Test it
print("Testing with updated prompt:")
try:
    result = retrieval_grader.invoke({"question": "What color is the sky?", "document": "The sky is blue during the day."})
    print(f"Success! Result: {result}")
    print(f"binary_score value: {result.binary_score}")
except Exception as e:
    print(f"Error: {e}")
