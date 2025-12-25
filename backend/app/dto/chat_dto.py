from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class MessageDTO(BaseModel):
    id: int
    sender: str
    content: str
    created_at: datetime

class ChatInitRequest(BaseModel):
    user_id: Optional[int] = None  

class ChatMessageRequest(BaseModel):
    user_id: int
    message: str

class ChatInitData(BaseModel):
    user_id: int
    message: MessageDTO

class ChatHistoryDTO(BaseModel):
    messages: list[MessageDTO]
    has_more: bool
