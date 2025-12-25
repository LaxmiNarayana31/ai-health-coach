from pydantic import BaseModel
from typing import List
from datetime import datetime

class HistoryMessageDTO(BaseModel):
    id: int
    sender: str
    content: str
    created_at: datetime

class HistoryData(BaseModel):
    messages: List[HistoryMessageDTO]
    has_more: bool