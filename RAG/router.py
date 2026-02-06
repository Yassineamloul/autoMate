from typing import Literal
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_ollama import ChatOllama

# 1. Data model - Constrained to ONLY vectorstore
class RouteQuery(BaseModel):
    """Route a user query to the most relevant datasource."""
    datasource: Literal["vectorstore"] = Field(
        description="The destination for the user query. Must always be 'vectorstore'."
    )

# 2. LLM Configuration 
# Adding format="json" helps Llama 3.2 adhere strictly to the Pydantic schema
llm = ChatOllama(model="gpt-oss:120b-cloud", temperature=0.0, format="json")
structured_llm_router = llm.with_structured_output(RouteQuery)

# 3. Updated System Prompt
# Explicitly telling the model to ignore outside knowledge and force the route
system = """You are a specialized router. 
Your ONLY job is to route every single user question to the 'vectorstore'.
Do not answer the question. Do not provide commentary. 
Even if the question is off-topic, your output must be the vectorstore datasource."""

route_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "{question}"),
    ]
)

# 4. Chain
question_router = route_prompt | structured_llm_router

# Test 1: Off-topic question
print("NFL Question Route:")
print(question_router.invoke({"question": "Who will the Bears draft first in the NFL draft?"}))

# Test 2: On-topic question
print("\nAgent Memory Question Route:")
print(question_router.invoke({"question": "What are the types of agent memory?"}))