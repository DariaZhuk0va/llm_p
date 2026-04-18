from datetime import datetime
from typing import List, Optional

from sqlalchemy import String, DateTime, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.base import Base
from app.schemas.user import UserRole


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
                                primary_key=True,
                                index=True
                                )
    email: Mapped[str] = mapped_column(
                                String(50),
                                unique=True,
                                index=True,
                                nullable=False
                                )
    password_hash: Mapped[str] = mapped_column(
                                String(255),
                                nullable=False
                                )
    role: Mapped[UserRole] = mapped_column(
                                String(20),
                                default=UserRole.USER,
                                nullable=False)
    created_at: Mapped[datetime] = mapped_column(
                                DateTime(timezone=True),
                                server_default=func.now()
                                )

    messages: Mapped[List["ChatMessage"]] = relationship(
        "ChatMessage",
        back_populates="user",
        cascade="all, delete-orphan"
    )


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id: Mapped[int] = mapped_column(
                                primary_key=True,
                                index=True
                                )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id",
                                           ondelete="CASCADE"),
                                           nullable=False)
    role: Mapped[str] = mapped_column(
                                String(20),
                                nullable=False
                                )
    content: Mapped[str] = mapped_column(
                                String(4096),
                                nullable=False
                                )
    created_at: Mapped[datetime] = mapped_column(
                                DateTime(timezone=True),
                                server_default=func.now()
                                )

    user: Mapped["User"] = relationship(
                                "User",
                                back_populates="messages"
                                )