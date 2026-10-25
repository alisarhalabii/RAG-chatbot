import os
from pathlib import Path

from dotenv import load_dotenv

# Load variables from a local .env file if present (used for local dev / API keys)
load_dotenv()

# the root directory of this project
ROOT_DIR = Path(__file__).resolve().parent.parent.parent

# defining data
RAW_DATA_DIR = ROOT_DIR / "data" / "raw"
CHROMA_DIR = ROOT_DIR / "data" / "chroma"

# embedding model that is running locally, no api key needed
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# chunking parameters
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# --- LLM configuration ---
# "groq" = cloud LLM (fast + free tier, used for the deployed/live version)
# "ollama" = local LLM (used for offline development, requires Ollama running)
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")

# comma-separated list of frontend origins allowed to call the API (CORS)
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
