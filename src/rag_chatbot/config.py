from pathlib import Path

# the root directory of this project
ROOT_DIR= Path(__file__).resolve().parent.parent.parent

#defining data
RAW_DATA_DIR= ROOT_DIR / "data" / "raw"
CHROMA_DIR = ROOT_DIR / "data" / "chroma"

#embedding model that is running locally no api keys
EMBEDDING_MODEL= "all-MiniLM-L6-v2"

#chunking parameters
CHUNKS_SIZE= 500
CHUNK_OVERLAP= 50
