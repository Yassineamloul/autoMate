from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_community.document_loaders import (
    WebBaseLoader,
    PyPDFLoader,
    CSVLoader,
)

from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings


# -----------------------
# Embeddings
# -----------------------
embd = OllamaEmbeddings(
    model="embeddinggemma",
    base_url="http://localhost:11434",
)

# -----------------------
# Base data folders
# -----------------------
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
PDF_DIR = DATA_DIR / "pdf"
CSV_DIR = DATA_DIR / "csv"

# -----------------------
# Optional URLs
# -----------------------
urls = [
    "https://www.microsoft.com/en-us/legal/terms-of-use?utm_source=chatgpt.com",
    "https://www.microsoft.com/en-gb/privacy/privacystatement?utm_source=chatgpt.com",
    "https://learn.microsoft.com/en-us/power-platform/admin/governance-considerations?utm_source=chatgpt.com",
]

# -----------------------
# Loaders
# -----------------------
def load_from_urls(urls_list):
    docs_nested = [WebBaseLoader(url).load() for url in urls_list]
    return [d for sub in docs_nested for d in sub]


def load_from_pdfs(folder: Path):
    docs = []
    if folder.exists():
        for pdf_path in folder.glob("*.pdf"):
            loader = PyPDFLoader(str(pdf_path))
            docs.extend(loader.load())  # one Document per page
    return docs


def load_from_csvs(folder: Path):
    docs = []
    if folder.exists():
        for csv_path in folder.glob("*.csv"):
            loader = CSVLoader(file_path=str(csv_path))
            docs.extend(loader.load())  # one Document per row
    return docs


# -----------------------
# Build documents list
# -----------------------
docs_list = []

if urls:
    docs_list.extend(load_from_urls(urls))

docs_list.extend(load_from_pdfs(PDF_DIR))
docs_list.extend(load_from_csvs(CSV_DIR))

if not docs_list:
    raise ValueError(
        "No documents found. Add PDFs to data/pdf/, CSVs to data/csv/, or URLs."
    )

# -----------------------
# Split documents
# -----------------------
text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=800,
    chunk_overlap=120,
)
doc_splits = text_splitter.split_documents(docs_list)

# -----------------------
# Vectorstore
# -----------------------
vectorstore = Chroma.from_documents(
    documents=doc_splits,
    collection_name="rag-chroma",
    embedding=embd,
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

if __name__ == "__main__":
    # Optional local test (won't run on import)
    question = "What are the governance considerations for Power Platform?"
    retrieved_docs = retriever.invoke(question)
    print(f"Retrieved {len(retrieved_docs)} documents:")
    for doc in retrieved_docs:
        print(f"- {doc.metadata.get('source', 'no source')} - {doc.page_content[:100]}...")