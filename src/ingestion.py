from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.config import (
    KNOWLEDGE_BASE_PATH,
    VECTORSTORE_PATH,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    EMBEDDING_MODEL,
)


def load_documents():

    print("Loading knowledge base...")

    loader = PyPDFLoader(str(KNOWLEDGE_BASE_PATH))
    documents = loader.load()

    print(f"Loaded {len(documents)} pages.")

    return documents


def split_documents(documents):
    print("Splitting documents into chunks...")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )

    chunks = splitter.split_documents(documents)

    print(f"Created {len(chunks)} chunks.")

    return chunks


def create_embeddings():
    print("Loading embedding model...")

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )

    print("Embedding model loaded.")

    return embeddings


def build_vectorstore(chunks, embeddings):
   
    print("Building FAISS vector store...")

    vectorstore = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings,
    )

    vectorstore_path = Path(VECTORSTORE_PATH)
    vectorstore_path.mkdir(parents=True, exist_ok=True)

    vectorstore.save_local(str(vectorstore_path))

    print(f"Vector store saved to: {vectorstore_path}")

    return vectorstore


def main():
    documents = load_documents()

    chunks = split_documents(documents)

    embeddings = create_embeddings()

    build_vectorstore(
        chunks=chunks,
        embeddings=embeddings,
    )

    print("\nIngestion completed successfully.")


if __name__ == "__main__":
    main()