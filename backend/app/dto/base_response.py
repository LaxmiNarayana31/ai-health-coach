from typing import Generic, Optional, TypeVar
from pydantic import BaseModel

T = TypeVar("T")

class APIError(BaseModel):
    code: str
    detail: str

class APIResponse(BaseModel, Generic[T]):
    status: bool
    message: str
    data: Optional[T] = None
    error: Optional[APIError] = None
