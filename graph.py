from typing import List
from typing_extensions import TypedDict
from pprint import pprint

from langchain_core.documents import Document
from langgraph.graph import END, StateGraph, START

# ✅ Imports depuis tes fichiers RAG
from RAG.index import retriever                 # retriever = vectorstore.as_retriever()
from RAG.generator import rag_chain, format_docs # rag_chain = prompt | llm | StrOutputParser()
from RAG.grader1 import retrieval_grader     # relevance grader (doc vs question)
from RAG.grader2 import answer_grader
from RAG.hallucinate_detector import hallucination_grader     # hallucination grader (generation vs docs)
from RAG.answer_rewriter import question_rewriter # rewrite question


class GraphState(TypedDict):
    """
    State du graph.
    """
    question: str
    generation: str
    documents: List[Document]
    retries: int


# ---------------------------
# Nodes
# ---------------------------

def retrieve(state: GraphState) -> GraphState:
    print("\n---RETRIEVE---")
    question = state["question"]
    documents = retriever.invoke(question)
    return {"question": question, "documents": documents, "generation": state.get("generation",""), "retries": state.get("retries",0)}


def grade_documents(state: GraphState) -> GraphState:
    print("\n---GRADE DOCUMENTS (RELEVANCE)---")
    question = state["question"]
    documents = state["documents"]

    filtered_docs = []
    for d in documents:
        score = retrieval_grader.invoke({"question": question, "document": d.page_content})
        if score.binary_score == "yes":
            filtered_docs.append(d)

    print(f"Docs kept: {len(filtered_docs)}/{len(documents)}")
    return {"question": question, "documents": filtered_docs, "generation": state.get("generation", ""), "retries": state.get("retries", 0)}


def transform_query(state: GraphState) -> GraphState:
    print("\n---TRANSFORM QUERY---")
    question = state["question"]
    documents = state["documents"]

    better_question = question_rewriter.invoke({"question": question})
    if hasattr(better_question, "content"):
        better_question = better_question.content

    return {
    "question": better_question,
    "documents": documents,
    "generation": state.get("generation", ""),
    "retries": state["retries"] + 1,
}


def generate(state: GraphState) -> GraphState:
    print("\n---GENERATE---")
    question = state["question"]
    documents = state["documents"]

    generation = rag_chain.invoke({
        "context": format_docs(documents),
        "question": question
    })
    if not documents:
        generation = (
        "No relevant evidence was found in the provided documents for this request. "
        "Try rephrasing the request or provide more specific process documents."
    )
    return {"question": question, "documents": documents, "generation": generation, "retries": state.get("retries", 0)}


# ---------------------------
# Conditional edges
# ---------------------------

MAX_RETRIES = 2

def decide_to_generate(state: GraphState) -> str:
    print("\n---DECIDE TO GENERATE---")

    if state["documents"]:
        print("Relevant docs found → generate")
        return "generate"

    if state["retries"] < MAX_RETRIES:
        print(f"No relevant docs → retry ({state['retries'] + 1}/{MAX_RETRIES})")
        return "transform_query"

    print("Retries exhausted → generate fallback")
    return "generate"



def grade_generation(state: GraphState) -> str:
    print("\n---GRADE GENERATION (HALLUCINATION + ANSWER)---")
    question = state["question"]
    documents = state["documents"]
    generation = state["generation"]

    # 1) grounded?
    grounded = hallucination_grader.invoke({
        "documents": format_docs(documents),
        "generation": generation
    }).binary_score

    if grounded != "yes":
        print("Not grounded → retry generate")
        return "not_supported"

    # 2) answers question?
    useful = answer_grader.invoke({
        "question": question,
        "generation": generation
    }).binary_score

    if useful == "yes":
        print("Useful answer → END")
        return "useful"

    print("Not useful → transform_query")
    return "not_useful"


# ---------------------------
# Build graph
# ---------------------------

workflow = StateGraph(GraphState)

workflow.add_node("retrieve", retrieve)
workflow.add_node("grade_documents", grade_documents)
workflow.add_node("transform_query", transform_query)
workflow.add_node("generate", generate)

workflow.add_edge(START, "retrieve")
workflow.add_edge("retrieve", "grade_documents")

workflow.add_conditional_edges(
    "grade_documents",
    decide_to_generate,
    {
        "transform_query": "transform_query",
        "generate": "generate",
    },
)

workflow.add_edge("transform_query", "retrieve")

workflow.add_conditional_edges(
    "generate",
    grade_generation,
    {
        "not_supported": "generate",        # retry
        "not_useful": "transform_query",    # rewrite question
        "useful": END,
    },
)

app = workflow.compile()


# ---------------------------
# Run (demo)
# ---------------------------
if __name__ == "__main__":
    inputs = {"question": "What processes in these documents can be automated (approvals, monitoring, audit logs, access control)?"}
    
    last_state = None
    for output in app.stream(inputs):
        for node_name, state in output.items():
            pprint(f"Node '{node_name}' done.")
            last_state = state

    print("\n=== FINAL ANSWER ===")
    print(last_state["generation"])
