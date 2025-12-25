from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from config.database import get_db
from app.services.history_service import HistoryService
from app.dto.history_dto import HistoryData, HistoryMessageDTO
from app.dto.base_response import APIResponse

router = APIRouter(prefix="/chat", tags=["History"])


@router.get("/history", response_model=APIResponse[HistoryData])
async def get_chat_history(user_id: int, before_id: int | None = Query(None), limit: int = Query(20, le=50), db: AsyncSession = Depends(get_db)):
    messages, has_more = await HistoryService.get_history(db, user_id, before_id, limit)

    return APIResponse(
        status=True,
        message="Chat history fetched successfully",
        data=HistoryData(
            messages=[
                HistoryMessageDTO(
                    id=m.id,
                    sender=m.sender,
                    content=m.content,
                    created_at=m.created_at
                )
                for m in messages
            ],
            has_more=has_more
        )
    )
