from sqlalchemy import create_engine
from dotenv import load_dotenv

import os
from pathlib import Path

# caminho absoluto da raiz do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# carregar .env
load_dotenv(BASE_DIR / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")

print(DATABASE_URL)

engine = create_engine(DATABASE_URL)