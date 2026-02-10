from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv

load_dotenv()

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

llm = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    temperature=1.0,
    thinking_level="low",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)
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
