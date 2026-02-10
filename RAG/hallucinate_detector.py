from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv

load_dotenv()



class GradeHallucinations(BaseModel):
    """Binary score for hallucination present in generation answer."""

    binary_score: str = Field(
        description="Answer is grounded in the facts, 'yes' or 'no'"
    )


# LLM with function call
llm = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    temperature=1.0,
    thinking_level="low",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)
structured_llm_grader = llm.with_structured_output(GradeHallucinations)

# Prompt
system = """You are a grader assessing whether an LLM generation is grounded in / supported by a set of retrieved facts. \n 
     Return ONLY a JSON object exactly like{{"binary_score":"yes"}} or {{"binary_score":"no"}}.
No other text. 'Yes' means that the answer is grounded in / supported by the set of facts."""
hallucination_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "Set of facts: \n\n {documents} \n\n LLM generation: {generation}"),
    ]
)

hallucination_grader = hallucination_prompt | structured_llm_grader
if __name__ == "__main__":
    # Local test (SAFE)
    documents = "Agent memory refers to short-term and long-term memory in LLM agents."
    generation = "Agent memory is a type of memory that allows agents to remember past interactions and learn from them."
    print(
        hallucination_grader.invoke(
            {"documents": documents, "generation": generation}
        )
    )