"""
AI conversation models
"""
from sqlalchemy import Column, String, Text, Integer, ForeignKey, JSON
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class Conversation(BaseModel):
    """
    AI conversation model for tracking chat sessions
    """

    __tablename__ = "conversations"

    # Conversation metadata
    session_id = Column(String(100), unique=True, nullable=False, index=True)
    user_id = Column(String(100), nullable=True, index=True)  # For multi-user systems

    # Conversation summary (AI-generated)
    summary = Column(Text, nullable=True)
    tags = Column(JSON, nullable=True)  # For categorizing conversations

    # Context tracking
    context_data = Column(JSON, nullable=True)  # Store relevant context

    # Relationships
    messages = relationship("ConversationMessage", back_populates="conversation", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Conversation(id={self.id}, session_id={self.session_id})>"


class ConversationMessage(BaseModel):
    """
    Individual messages in a conversation
    """

    __tablename__ = "conversation_messages"

    # Message details
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False, index=True)
    role = Column(String(20), nullable=False)  # user, assistant, system
    content = Column(Text, nullable=False)

    # Metadata
    tokens_used = Column(Integer, nullable=True)
    model_used = Column(String(50), nullable=True)
    metadata = Column(JSON, nullable=True)  # For storing additional info

    # Relationships
    conversation = relationship("Conversation", back_populates="messages")

    def __repr__(self) -> str:
        return f"<ConversationMessage(id={self.id}, conversation_id={self.conversation_id}, role={self.role})>"


class AIInsight(BaseModel):
    """
    AI-generated insights and recommendations
    """

    __tablename__ = "ai_insights"

    # Insight details
    insight_type = Column(String(50), nullable=False, index=True)  # warning, opportunity, recommendation
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    action = Column(String(255), nullable=True)
    priority = Column(String(20), default="medium")  # low, medium, high, critical

    # Context
    related_entity_type = Column(String(50), nullable=True)  # product, order, supplier, etc.
    related_entity_id = Column(Integer, nullable=True)
    metadata = Column(JSON, nullable=True)

    # Insight lifecycle
    is_active = Column(Integer, default=1)  # Boolean: is the insight still relevant?
    is_dismissed = Column(Integer, default=0)  # Boolean: user dismissed the insight
    dismissed_at = Column(String(100), nullable=True)  # Timestamp when dismissed

    def __repr__(self) -> str:
        return f"<AIInsight(id={self.id}, type={self.insight_type}, title={self.title})>"
