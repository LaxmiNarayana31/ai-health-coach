from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Index, func
from config.database import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    sender = Column(String(20), nullable=False)  
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        Index("idx_user_created_at", "user_id", "created_at"),
    )