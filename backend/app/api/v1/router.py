"""
Main API router
"""
from fastapi import APIRouter

from app.api.v1.endpoints import inventory, orders, analytics, ai_chat

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(
    ai_chat.router,
    prefix="/chat",
    tags=["AI Chat"]
)

api_router.include_router(
    inventory.router,
    prefix="/inventory",
    tags=["Inventory"]
)

api_router.include_router(
    orders.router,
    prefix="/orders",
    tags=["Orders"]
)

api_router.include_router(
    analytics.router,
    prefix="/analytics",
    tags=["Analytics"]
)
