from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field


# ---------------------------
# Data model
# ---------------------------

class GradeAnswer(BaseModel):
    """Binary score to assess whether the answer addresses the question."""
    binary_score: str = Field(
        description="Answer addresses the question, 'yes' or 'no'"
    )


# ---------------------------
# LLM
# ---------------------------

llm = ChatOllama(model="gpt-oss:120b-cloud", temperature=0, format="json")
structured_llm_grader = llm.with_structured_output(GradeAnswer)


# ---------------------------
# Prompt
# ---------------------------

system = """You are a grader assessing whether an answer addresses / resolves a question.
Return ONLY a JSON object exactly like {{"binary_score":"yes"}} or {{"binary_score":"no"}}.
No other text.
'Yes' means that the answer resolves the question.
"""

answer_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "User question:\n\n{question}\n\nLLM generation:\n\n{generation}"),
    ]
)


# ✅ Export utilisé par graph.py
answer_grader = answer_prompt | structured_llm_grader


# ---------------------------
# Local test (SAFE)
# ---------------------------

if __name__ == "__main__":
    question = "What is agent memory?"
    generation = "Agent memory refers to short-term and long-term memory in LLM agents."

    print(
        answer_grader.invoke({
            "question": question,
            "generation": generation
        })
    )
