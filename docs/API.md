
# API Documentation

Complete API reference for the WWS Inventory Platform.

## Base URL

- **Development**: `http://localhost:8000/api/v1`
- **Production**: `https://your-domain.com/api/v1`

## Authentication

Currently, the API is open for development. Production will use JWT authentication.

**Planned Authentication Flow:**
```
POST /api/v1/auth/login
{
  "email": "user@example.com",
  "password": "password"
}

Response:
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer",
  "expires_in": 1800
}

# Use token in subsequent requests:
Authorization: Bearer eyJhbGc...
```

## Endpoints

### AI Chat

#### Send Message
```http
POST /api/v1/chat/message
Content-Type: application/json

{
  "message": "What's in stock?",
  "conversation_id": "optional-session-id"
}
```

**Response:**
```json
{
  "message": "Here are your current stock levels...",
  "conversation_id": "conv-123",
  "suggestions": [
    "Show me low stock items",
    "What are today's orders?",
    "Create a purchase order"
  ]
}
```

#### Get Conversation History
```http
GET /api/v1/chat/history/{conversation_id}
```

**Response:**
```json
{
  "conversation_id": "conv-123",
  "messages": [
    {
      "role": "user",
      "content": "What's in stock?",
      "timestamp": "2024-01-15T10:30:00Z"
    },
    {
      "role": "assistant",
      "content": "Here are your current stock levels...",
      "timestamp": "2024-01-15T10:30:02Z"
    }
  ]
}
```

---

### Inventory Management

#### List Products
```http
GET /api/v1/inventory/products?skip=0&limit=100
```

**Query Parameters:**
- `skip` (int): Number of records to skip (pagination)
- `limit` (int): Maximum records to return

**Response:**
```json
[
  {
    "id": 1,
    "name": "Laptop Computer",
    "sku": "LAP-001",
    "description": "High-performance laptop",
    "category": "Electronics",
    "price": 1499.99,
    "stock_quantity": 25,
    "reorder_point": 10
  }
]
```

#### Get Product
```http
GET /api/v1/inventory/products/{product_id}
```

**Response:**
```json
{
  "id": 1,
  "name": "Laptop Computer",
  "sku": "LAP-001",
  "description": "High-performance laptop",
  "category": "Electronics",
  "price": 1499.99,
  "stock_quantity": 25,
  "reorder_point": 10,
  "warehouse_location": "A-12",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

#### Create Product
```http
POST /api/v1/inventory/products
Content-Type: application/json

{
  "name": "Wireless Mouse",
  "sku": "MOU-001",
  "description": "Ergonomic wireless mouse",
  "category": "Electronics",
  "price": 29.99,
  "stock_quantity": 100,
  "reorder_point": 20
}
```

**Response:** (201 Created)
```json
{
  "id": 2,
  "name": "Wireless Mouse",
  "sku": "MOU-001",
  ...
}
```

#### Get Low Stock Items
```http
GET /api/v1/inventory/low-stock
```

**Response:**
```json
[
  {
    "id": 3,
    "name": "Desk Lamp",
    "sku": "LAM-001",
    "stock_quantity": 5,
    "reorder_point": 20,
    "status": "critical"
  }
]
```

---

### Order Management

#### List Orders
```http
GET /api/v1/orders?skip=0&limit=100&status=pending
```

**Query Parameters:**
- `skip` (int): Pagination offset
- `limit` (int): Maximum records
- `status` (string): Filter by status (pending, processing, shipped, delivered, cancelled)

**Response:**
```json
[
  {
    "id": 1,
    "order_number": "ORD-2024-001",
    "customer_name": "John Smith",
    "total_amount": 1599.98,
    "status": "processing",
    "created_at": "2024-01-15T09:00:00Z"
  }
]
```

#### Get Order
```http
GET /api/v1/orders/{order_id}
```

**Response:**
```json
{
  "id": 1,
  "order_number": "ORD-2024-001",
  "customer_name": "John Smith",
  "customer_email": "john@example.com",
  "status": "processing",
  "items": [
    {
      "id": 1,
      "product_name": "Laptop Computer",
      "product_sku": "LAP-001",
      "quantity": 1,
      "unit_price": 1499.99,
      "subtotal": 1499.99
    }
  ],
  "subtotal": 1499.99,
  "tax": 149.99,
  "shipping_cost": 15.00,
  "total_amount": 1664.98,
  "created_at": "2024-01-15T09:00:00Z"
}
```

#### Create Order
```http
POST /api/v1/orders
Content-Type: application/json

{
  "customer_name": "Jane Doe",
  "customer_email": "jane@example.com",
  "items": [
    {
      "product_id": 1,
      "quantity": 2,
      "unit_price": 29.99
    }
  ],
  "notes": "Express delivery requested"
}
```

**Response:** (201 Created)
```json
{
  "id": 2,
  "order_number": "ORD-2024-002",
  "customer_name": "Jane Doe",
  "total_amount": 59.98,
  "status": "pending",
  "created_at": "2024-01-15T10:00:00Z"
}
```

#### Update Order Status
```http
PATCH /api/v1/orders/{order_id}/status
Content-Type: application/json

{
  "status": "shipped"
}
```

**Valid Statuses:**
- `pending` - Order placed, awaiting processing
- `processing` - Order being prepared
- `shipped` - Order dispatched
- `delivered` - Order received by customer
- `cancelled` - Order cancelled

---

### Analytics

#### Get Dashboard Metrics
```http
GET /api/v1/analytics/dashboard
```

**Response:**
```json
{
  "total_products": 1234,
  "low_stock_items": 23,
  "total_value": 245678.50,
  "pending_orders": 45,
  "revenue_today": 12500.00,
  "revenue_this_month": 185000.00
}
```

#### Get Sales Trends
```http
GET /api/v1/analytics/sales/trends?days=30
```

**Response:**
```json
[
  {
    "date": "2024-01-15",
    "revenue": 12500.00,
    "orders": 45,
    "units_sold": 234
  },
  {
    "date": "2024-01-14",
    "revenue": 11200.00,
    "orders": 42,
    "units_sold": 198
  }
]
```

#### Get Top Sellers
```http
GET /api/v1/analytics/products/top-sellers?limit=10&period=week
```

**Response:**
```json
[
  {
    "product_id": 1,
    "product_name": "Laptop Computer",
    "units_sold": 234,
    "revenue": 350766.66,
    "growth_rate": 0.45
  }
]
```

#### Get AI Insights
```http
GET /api/v1/analytics/insights
```

**Response:**
```json
[
  {
    "type": "warning",
    "title": "Low Stock Alert",
    "message": "Product A will run out in 2 days at current rate",
    "action": "Create Purchase Order",
    "priority": "high"
  },
  {
    "type": "opportunity",
    "title": "Seasonal Trend",
    "message": "Detected seasonal pattern for holidays",
    "action": "View Forecast",
    "priority": "medium"
  }
]
```

#### Forecast Demand
```http
GET /api/v1/analytics/forecast/demand?product_id=1&days_ahead=30
```

**Response:**
```json
{
  "product_id": 1,
  "forecast_period": 30,
  "predictions": [
    {
      "date": "2024-01-16",
      "predicted_demand": 8,
      "confidence": 0.87
    }
  ],
  "confidence": 0.85
}
```

---

## Error Responses

All errors follow this format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

**Common HTTP Status Codes:**
- `200 OK` - Request successful
- `201 Created` - Resource created successfully
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource doesn't exist
- `422 Unprocessable Entity` - Validation error
- `500 Internal Server Error` - Server error

**Example Error:**
```json
{
  "detail": "Product with SKU 'LAP-001' already exists"
}
```

---

## Rate Limiting

**Current Limits:**
- 100 requests per minute per IP
- 1000 requests per hour per IP

**Rate Limit Headers:**
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1234567890
```

---

## Pagination

List endpoints support pagination:

```http
GET /api/v1/inventory/products?skip=0&limit=20
```

**Response Headers:**
```
X-Total-Count: 1234
X-Page-Size: 20
X-Current-Page: 1
```

---

## Webhooks (Coming Soon)

Subscribe to events:
- `order.created`
- `order.updated`
- `stock.low`
- `stock.out`

---

## SDKs

**Official SDKs:**
- Python SDK (coming soon)
- JavaScript/TypeScript SDK (coming soon)
- Go SDK (coming soon)

**Example Usage:**
```python
from wws_inventory import WWS

client = WWS(api_key="your-key")
products = client.products.list(limit=10)
```

---

## Interactive Documentation

For interactive API testing, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## Support

- **Issues**: https://github.com/Afinucci/Afinucci.github.io/issues
- **API Status**: https://status.yourplatform.com
- **Changelog**: See `CHANGELOG.md`
