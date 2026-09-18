from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from src.config import (
    VECTORSTORE_PATH,
    EMBEDDING_MODEL,
    TOP_K,
)


def load_vectorstore():
    print("Loading vector store...")

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )

    vectorstore = FAISS.load_local(
        VECTORSTORE_PATH,
        embeddings,
        allow_dangerous_deserialization=True,
    )

    print("Vector store loaded.")

    return vectorstore


def retrieve_documents(query: str, top_k: int = TOP_K):

    vectorstore = load_vectorstore()

    documents = vectorstore.similarity_search(
        query,
        k=top_k,
    )

    return documents


def main():


    query = input("\nEnter your question: ")

    documents = retrieve_documents(query)

    print(f"\nRetrieved {len(documents)} relevant documents:\n")

    for i, document in enumerate(documents, start=1):
        print(f"--- Result {i} ---")
        print(f"Page: {document.metadata.get('page', 'Unknown') + 1}")
        print(document.page_content)
        print()


if __name__ == "__main__":
    main()