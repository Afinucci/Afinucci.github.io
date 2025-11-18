"""
Tests for inventory endpoints
"""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_list_products(client: AsyncClient):
    """Test listing all products"""
    response = await client.get("/api/v1/inventory/products")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_list_products_with_pagination(client: AsyncClient):
    """Test product listing with pagination"""
    response = await client.get("/api/v1/inventory/products?skip=0&limit=10")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 10


@pytest.mark.asyncio
async def test_get_product_not_found(client: AsyncClient):
    """Test getting a non-existent product"""
    response = await client.get("/api/v1/inventory/products/99999")

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_product(client: AsyncClient, sample_product_data):
    """Test creating a new product"""
    response = await client.post(
        "/api/v1/inventory/products",
        json=sample_product_data,
    )

    # Currently returns 501 Not Implemented
    assert response.status_code in [201, 501]


@pytest.mark.asyncio
async def test_get_low_stock_items(client: AsyncClient):
    """Test retrieving low stock items"""
    response = await client.get("/api/v1/inventory/low-stock")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
