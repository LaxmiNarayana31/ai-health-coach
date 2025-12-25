import os
import json
from pathlib import Path

from dotenv import load_dotenv
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv(verbose=True)

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set in environment variables")

# Connection pool settings
POOL_SIZE = 20
MAX_OVERFLOW = 2
POOL_TIMEOUT = 15
POOL_RECYCLE = 3600

# Create async engine
engine_kwargs = {
    "pool_timeout": POOL_TIMEOUT,
    "pool_recycle": POOL_RECYCLE,
    "echo": False
}

if "sqlite" in DATABASE_URL:
    engine_kwargs["connect_args"] = {"check_same_thread": False}
else:
    engine_kwargs["pool_size"] = POOL_SIZE
    engine_kwargs["max_overflow"] = MAX_OVERFLOW

engine = create_async_engine(
    DATABASE_URL,
    **engine_kwargs
)

# Base model
Base = declarative_base()

# Async session factory
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)

# Dependency for FastAPI
async def get_db():
    async with AsyncSessionLocal() as db:
        try:
            yield db
        except Exception as ex:
            print("Error getting DB session:", ex)
            raise
        finally:
            await db.close()

def response(status: bool, message: str, data):
    return {
        "status": status,
        "message": message,
        "data": data,
    }