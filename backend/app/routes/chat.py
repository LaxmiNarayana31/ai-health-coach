from fastapi import APIRouter, Depends
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from config.database import get_db
from app.services.chat_service import ChatService
from app.services.history_service import HistoryService
from app.dto.chat_dto import (
    ChatInitRequest,
    ChatInitData,
    ChatMessageRequest,
    MessageDTO,
    ChatHistoryDTO
)
from app.dto.base_response import APIResponse, APIError

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/init", response_model=APIResponse[ChatInitData])
async def init_chat(payload: ChatInitRequest, db: AsyncSession = Depends(get_db)):
    message, user_id = await ChatService.init_chat(db, payload.user_id)

    return APIResponse(
        status=True,
        message="Chat initialized successfully",
        data=ChatInitData(
            user_id=user_id,
            message=MessageDTO(
                id=message.id,
                sender=message.sender,
                content=message.content,
                created_at=message.created_at
            )
        )
    )


@router.post("/message", response_model=APIResponse[MessageDTO])
async def send_message(payload: ChatMessageRequest, db: AsyncSession = Depends(get_db)):
    if not payload.message.strip():
        return APIResponse(
            status=False,
            message="Validation error",
            error=APIError(
                code="EMPTY_MESSAGE",
                detail="Message cannot be empty"
            )
        )

    msg = await ChatService.send_message(db=db, user_id=payload.user_id, user_message=payload.message)

    return APIResponse(
        status=True,
        message="Message processed successfully",
        data=MessageDTO(
            id=msg.id,
            sender=msg.sender,
            content=msg.content,
            created_at=msg.created_at
        )
    )


@router.get("/history", response_model=APIResponse[ChatHistoryDTO])
async def get_history(user_id: int, before_id: Optional[int] = None, limit: int = 20, db: AsyncSession = Depends(get_db)):
    messages, has_more = await HistoryService.get_history(db, user_id, before_id, limit)

    msg_dtos = [
        MessageDTO(
            id=m.id,
            sender=m.sender,
            content=m.content,
            created_at=m.created_at
        ) for m in messages
    ]

    return APIResponse(
        status=True,
        message="History fetched successfully",
        data=ChatHistoryDTO(
            messages=msg_dtos,
            has_more=has_more
        )
    )
