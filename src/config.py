import os

from dotenv import load_dotenv
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL")


EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"


PROJECT_NAME = "LumaCart Smart Customer-Support Bot"

KNOWLEDGE_BASE_PATH = (
    "data/LumaCart_Company_Knowledge_Base.pdf"
)

VECTORSTORE_PATH = "vectorstore"


CHUNK_SIZE = 500

CHUNK_OVERLAP = 50

TOP_K = 10

RERANK_TOP_N = 4