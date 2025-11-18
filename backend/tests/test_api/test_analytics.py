"""
Tests for analytics endpoints
"""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_dashboard_metrics(client: AsyncClient):
    """Test retrieving dashboard metrics"""
    response = await client.get("/api/v1/analytics/dashboard")

    assert response.status_code == 200
    data = response.json()
    assert "total_products" in data
    assert "low_stock_items" in data
    assert "total_value" in data
    assert isinstance(data["total_products"], int)
    assert isinstance(data["total_value"], float)


@pytest.mark.asyncio
async def test_get_sales_trends(client: AsyncClient):
    """Test retrieving sales trends"""
    response = await client.get("/api/v1/analytics/sales/trends?days=30")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_get_top_sellers(client: AsyncClient):
    """Test retrieving top selling products"""
    response = await client.get("/api/v1/analytics/products/top-sellers?limit=10")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_get_ai_insights(client: AsyncClient):
    """Test retrieving AI-generated insights"""
    response = await client.get("/api/v1/analytics/insights")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

    # Check structure of insights
    if len(data) > 0:
        insight = data[0]
        assert "type" in insight
        assert "title" in insight
        assert "message" in insight
        assert "priority" in insight
        assert insight["type"] in ["warning", "opportunity", "recommendation"]


@pytest.mark.asyncio
async def test_forecast_demand(client: AsyncClient):
    """Test demand forecasting"""
    response = await client.get(
        "/api/v1/analytics/forecast/demand?product_id=1&days_ahead=30"
    )

    assert response.status_code == 200
    data = response.json()
    assert "product_id" in data
    assert "forecast_period" in data
    assert "predictions" in data
    assert "confidence" in data
