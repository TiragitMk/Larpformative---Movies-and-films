import os
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).parent.parent

load_dotenv(ROOT / ".env")
DB_PATH = ROOT / os.getenv("DB_PATH", "cine.db")

load_dotenv(ROOT / ".env") # Esta línea parece innecesaria pero me está dando error si no la uso.
API_URL = os.getenv("API_URL")
