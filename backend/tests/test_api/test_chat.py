"""
Tests for AI chat endpoints
"""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_send_message(client: AsyncClient):
    """Test sending a message to AI chat"""
    response = await client.post(
        "/api/v1/chat/message",
        json={
            "message": "What's in stock?",
            "conversation_id": None,
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "conversation_id" in data
    assert "suggestions" in data
    assert isinstance(data["suggestions"], list)


@pytest.mark.asyncio
async def test_send_message_with_conversation_id(client: AsyncClient):
    """Test sending a message with existing conversation ID"""
    response = await client.post(
        "/api/v1/chat/message",
        json={
            "message": "Show me low stock items",
            "conversation_id": "test-123",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["conversation_id"] == "test-123"


@pytest.mark.asyncio
async def test_get_conversation_history(client: AsyncClient):
    """Test retrieving conversation history"""
    conversation_id = "test-conversation-001"

    response = await client.get(f"/api/v1/chat/history/{conversation_id}")

    assert response.status_code == 200
    data = response.json()
    assert "conversation_id" in data
    assert "messages" in data
    assert isinstance(data["messages"], list)


@pytest.mark.asyncio
async def test_send_empty_message(client: AsyncClient):
    """Test that empty messages are rejected"""
    response = await client.post(
        "/api/v1/chat/message",
        json={
            "message": "",
            "conversation_id": None,
        },
    )

    # Should fail validation
    assert response.status_code in [422, 400]
