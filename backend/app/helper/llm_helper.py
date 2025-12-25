import os
from dotenv import load_dotenv
from app.core.memori import memori
from google.genai import Client as GoogleClient

load_dotenv(verbose=True)

def gemini_llm_with_memory(user_id: int):
    client = GoogleClient(api_key=os.getenv("GOOGLE_API_KEY"))

    # Register with Memori
    mem = memori.llm.register(client)
    mem.attribution(
        entity_id=f"user_{user_id}",
        process_id=f"disha_chat_{user_id}"
    )

    return client