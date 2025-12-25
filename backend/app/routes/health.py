from fastapi import APIRouter
from app.dto.base_response import APIResponse
from datetime import datetime

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("", response_model=APIResponse[dict])
async def health_check():
    return APIResponse(
        status=True,
        message="Service is healthy",
        data={
            "service": "disha-api",
            "timestamp": datetime.utcnow().isoformat()
        }
    )
