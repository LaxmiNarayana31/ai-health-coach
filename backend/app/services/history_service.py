import logging
import traceback

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.message import Message


class HistoryService:
    @staticmethod
    async def get_history(db: AsyncSession, user_id: int, before_id: int | None, limit: int):
        try:
            query = select(Message).where(Message.user_id == user_id)

            if before_id:
                query = query.where(Message.id < before_id)

            query = query.order_by(Message.id.desc()).limit(limit + 1)

            result = await db.execute(query)
            messages = result.scalars().all()

            has_more = len(messages) > limit
            messages = messages[:limit]

            messages.reverse()

            return messages, has_more
        except Exception as e:
            # Get the traceback as a string
            traceback_str = traceback.format_exc()
            logging.error(traceback_str)

            # Get the line number of the exception
            line_no = traceback.extract_tb(e.__traceback__)[-1][1]
            logging.error(f"Exception occurred on line {line_no}")

    @staticmethod
    async def get_context_messages(db: AsyncSession, user_id: int, limit: int = 10):
        try:
            """
            Fetches the last N messages for LLM context, ascending order.
            """
            query = select(Message).where(Message.user_id == user_id)\
                .order_by(Message.id.desc())\
                .limit(limit)
            
            result = await db.execute(query)
            messages = result.scalars().all()
            
            # Reverse to get chronological order (oldest -> newest) for the LLM
            return sorted(messages, key=lambda m: m.id)
        except Exception as e:
            # Get the traceback as a string
            traceback_str = traceback.format_exc()
            logging.error(traceback_str)

            # Get the line number of the exception
            line_no = traceback.extract_tb(e.__traceback__)[-1][1]
            logging.error(f"Exception occurred on line {line_no}")
