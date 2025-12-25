import os
from dotenv import load_dotenv
from memori import Memori
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv(verbose=True)

DATABASE_URL = os.getenv("DATABASE_URL")

SYNC_DATABASE_URL = DATABASE_URL.replace("+asyncpg", "").replace("+aiosqlite", "")

engine_kwargs = {"pool_pre_ping": True}
if "sqlite" in SYNC_DATABASE_URL:
    engine_kwargs["connect_args"] = {"check_same_thread": False}

engine = create_engine(
    SYNC_DATABASE_URL,
    **engine_kwargs
)

SessionLocal = sessionmaker(bind=engine)

# Global Memori instance
memori = Memori(conn=SessionLocal)
