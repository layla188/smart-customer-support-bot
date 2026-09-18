from langchain_openai import ChatOpenAI

from src.config import (
    OPENROUTER_API_KEY,
    OPENROUTER_MODEL,
)


def create_llm():

    llm = ChatOpenAI(   
        model=OPENROUTER_MODEL,
        api_key=OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1",
        temperature=0,
    )

    return llm


def main():

    llm = create_llm()

    print("LLM initialized successfully.")
    print(f"Model: {OPENROUTER_MODEL}")


if __name__ == "__main__":
    main()