from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")
API_URL = os.getenv("API_URL")

if not API_KEY:
    raise RuntimeError("API key no encontrada. Consulta 'README.md' y vuelve a intentarlo.")