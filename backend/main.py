import warnings
import uvicorn
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

import app.models
from app.core.memori import memori
from config.database import Base, engine
from app.routes.chat import router as chat_router
from app.routes.health import router as health_router
from app.routes.history import router as history_router

warnings.filterwarnings("ignore")

load_dotenv(verbose=True)
from app.utils.loader import check_env_vars
check_env_vars()

# Initialize FastAPI app
app = FastAPI(
    title="Disha - AI Health Coach API",
    description="Backend API for Disha, a WhatsApp-like AI health coach",
    version="1.0.0",
)

@app.on_event("startup")
async def init_memori_tables():
    memori.config.storage.build()

@app.on_event("startup")
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router registration
app.include_router(health_router)
app.include_router(chat_router)
app.include_router(history_router)

# Run the app
if __name__ == "__main__":
    port = int(os.getenv("PORT", 7000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info",
    )
    print("Server running on http://0.0.0.0:7000")


# if __name__ == "__main__":
#     port = int(os.getenv("PORT", 8000))
#     uvicorn.run(
#         "main:app",
#         host="0.0.0.0",
#         port=port,
#         reload=False,
#     )