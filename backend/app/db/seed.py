"""
Database seeding script for development and testing
"""
import asyncio
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import AsyncSessionLocal
from app.models.product import Product, ProductCategory, StockMovement
from app.models.order import Order, OrderItem, OrderStatus
from app.models.conversation import Conversation, ConversationMessage, AIInsight


async def seed_database():
    """Seed the database with sample data"""
    async with AsyncSessionLocal() as db:
        try:
            print("🌱 Starting database seeding...")

            # Create product categories
            categories = [
                ProductCategory(
                    name="Electronics",
                    description="Electronic devices and accessories",
                ),
                ProductCategory(
                    name="Office Supplies",
                    description="Office and stationery items",
                ),
                ProductCategory(
                    name="Furniture",
                    description="Office and home furniture",
                ),
            ]
            db.add_all(categories)
            await db.flush()
            print("✓ Created product categories")

            # Create sample products
            products = [
                Product(
                    name="Laptop Computer - Dell XPS 15",
                    sku="LAP-DEL-XPS15",
                    description="High-performance laptop for business use",
                    category="Electronics",
                    cost_price=1200.00,
                    selling_price=1499.99,
                    stock_quantity=25,
                    reorder_point=10,
                    reorder_quantity=20,
                    warehouse_location="A-12",
                    barcode="0123456789012",
                ),
                Product(
                    name="Wireless Mouse - Logitech MX Master 3",
                    sku="MOU-LOG-MX3",
                    description="Ergonomic wireless mouse",
                    category="Electronics",
                    cost_price=75.00,
                    selling_price=99.99,
                    stock_quantity=150,
                    reorder_point=50,
                    reorder_quantity=100,
                    warehouse_location="B-05",
                    barcode="0123456789013",
                ),
                Product(
                    name="Office Chair - Ergonomic Pro",
                    sku="FUR-CHA-ERG01",
                    description="Comfortable ergonomic office chair",
                    category="Furniture",
                    cost_price=200.00,
                    selling_price=299.99,
                    stock_quantity=45,
                    reorder_point=20,
                    reorder_quantity=30,
                    warehouse_location="C-08",
                ),
                Product(
                    name="Desk Lamp - LED Adjustable",
                    sku="OFF-LAM-LED01",
                    description="Energy-efficient LED desk lamp",
                    category="Office Supplies",
                    cost_price=25.00,
                    selling_price=39.99,
                    stock_quantity=8,  # Low stock for demo
                    reorder_point=20,
                    reorder_quantity=50,
                    warehouse_location="B-12",
                ),
                Product(
                    name="Notebook A4 - Premium",
                    sku="OFF-NOT-A4P",
                    description="Premium quality A4 notebooks",
                    category="Office Supplies",
                    cost_price=3.00,
                    selling_price=5.99,
                    stock_quantity=500,
                    reorder_point=100,
                    reorder_quantity=500,
                    warehouse_location="D-03",
                ),
            ]
            db.add_all(products)
            await db.flush()
            print(f"✓ Created {len(products)} products")

            # Create sample orders
            orders = [
                Order(
                    order_number="ORD-2024-001",
                    status=OrderStatus.DELIVERED,
                    customer_name="John Smith",
                    customer_email="john.smith@example.com",
                    customer_phone="+1234567890",
                    shipping_address_line1="123 Main Street",
                    shipping_city="New York",
                    shipping_state="NY",
                    shipping_postal_code="10001",
                    shipping_country="USA",
                    subtotal=1599.98,
                    tax=159.99,
                    shipping_cost=15.00,
                    total_amount=1774.97,
                    created_at=datetime.utcnow() - timedelta(days=5),
                ),
                Order(
                    order_number="ORD-2024-002",
                    status=OrderStatus.PROCESSING,
                    customer_name="Jane Doe",
                    customer_email="jane.doe@example.com",
                    customer_phone="+1234567891",
                    shipping_address_line1="456 Oak Avenue",
                    shipping_city="Los Angeles",
                    shipping_state="CA",
                    shipping_postal_code="90001",
                    shipping_country="USA",
                    subtotal=399.97,
                    tax=39.99,
                    shipping_cost=10.00,
                    total_amount=449.96,
                    created_at=datetime.utcnow() - timedelta(hours=6),
                ),
            ]
            db.add_all(orders)
            await db.flush()
            print(f"✓ Created {len(orders)} orders")

            # Create order items
            order_items = [
                # Order 1 items
                OrderItem(
                    order_id=orders[0].id,
                    product_id=products[0].id,
                    quantity=1,
                    unit_price=1499.99,
                    discount=0,
                    subtotal=1499.99,
                    product_name=products[0].name,
                    product_sku=products[0].sku,
                ),
                OrderItem(
                    order_id=orders[0].id,
                    product_id=products[1].id,
                    quantity=1,
                    unit_price=99.99,
                    discount=0,
                    subtotal=99.99,
                    product_name=products[1].name,
                    product_sku=products[1].sku,
                ),
                # Order 2 items
                OrderItem(
                    order_id=orders[1].id,
                    product_id=products[2].id,
                    quantity=1,
                    unit_price=299.99,
                    discount=0,
                    subtotal=299.99,
                    product_name=products[2].name,
                    product_sku=products[2].sku,
                ),
                OrderItem(
                    order_id=orders[1].id,
                    product_id=products[1].id,
                    quantity=1,
                    unit_price=99.99,
                    discount=0,
                    subtotal=99.99,
                    product_name=products[1].name,
                    product_sku=products[1].sku,
                ),
            ]
            db.add_all(order_items)
            print(f"✓ Created {len(order_items)} order items")

            # Create stock movements
            stock_movements = [
                StockMovement(
                    product_id=products[0].id,
                    movement_type="in",
                    quantity=30,
                    reference_type="purchase",
                    notes="Initial stock purchase",
                    performed_by="system",
                    created_at=datetime.utcnow() - timedelta(days=30),
                ),
                StockMovement(
                    product_id=products[0].id,
                    movement_type="out",
                    quantity=5,
                    reference_type="order",
                    reference_id=orders[0].id,
                    notes="Fulfilled order ORD-2024-001",
                    performed_by="system",
                    created_at=datetime.utcnow() - timedelta(days=5),
                ),
                StockMovement(
                    product_id=products[3].id,
                    movement_type="adjustment",
                    quantity=-12,
                    reference_type="adjustment",
                    notes="Stock count adjustment - damaged items",
                    performed_by="admin",
                    created_at=datetime.utcnow() - timedelta(days=2),
                ),
            ]
            db.add_all(stock_movements)
            print(f"✓ Created {len(stock_movements)} stock movements")

            # Create sample AI insights
            insights = [
                AIInsight(
                    insight_type="warning",
                    title="Low Stock Alert",
                    message="Desk Lamp - LED Adjustable (SKU: OFF-LAM-LED01) is critically low. Only 8 units remaining, below reorder point of 20.",
                    action="Create Purchase Order",
                    priority="high",
                    related_entity_type="product",
                    related_entity_id=products[3].id,
                    is_active=1,
                ),
                AIInsight(
                    insight_type="opportunity",
                    title="High Demand Product",
                    message="Wireless Mouse - Logitech MX Master 3 is selling 45% faster than last month. Consider increasing stock levels.",
                    action="Adjust Inventory Levels",
                    priority="medium",
                    related_entity_type="product",
                    related_entity_id=products[1].id,
                    is_active=1,
                ),
                AIInsight(
                    insight_type="recommendation",
                    title="Seasonal Stocking",
                    message="Based on historical patterns, office supplies typically see increased demand in September. Consider stocking up on notebooks and office supplies.",
                    action="View Forecast",
                    priority="medium",
                    is_active=1,
                ),
            ]
            db.add_all(insights)
            print(f"✓ Created {len(insights)} AI insights")

            # Create sample conversation
            conversation = Conversation(
                session_id="demo-session-001",
                user_id="demo-user",
                summary="Discussion about low stock items and reorder suggestions",
                tags=["inventory", "reorder", "alerts"],
            )
            db.add(conversation)
            await db.flush()

            messages = [
                ConversationMessage(
                    conversation_id=conversation.id,
                    role="user",
                    content="What items are low in stock?",
                ),
                ConversationMessage(
                    conversation_id=conversation.id,
                    role="assistant",
                    content="I found 1 item critically low in stock:\n\n• Desk Lamp - LED Adjustable (SKU: OFF-LAM-LED01)\n  Current: 8 units\n  Reorder point: 20 units\n  Status: ⚠️ CRITICAL\n\nWould you like me to create a purchase order for this item?",
                    tokens_used=156,
                    model_used="gpt-4",
                ),
                ConversationMessage(
                    conversation_id=conversation.id,
                    role="user",
                    content="Yes, create a PO for 50 units",
                ),
                ConversationMessage(
                    conversation_id=conversation.id,
                    role="assistant",
                    content="Purchase order created successfully!\n\n📄 PO-2024-001\n• Product: Desk Lamp - LED Adjustable\n• Quantity: 50 units\n• Estimated cost: $1,250.00\n• Supplier: Default Supplier\n• Expected delivery: 7-10 business days\n\nThe order has been sent to the supplier for confirmation.",
                    tokens_used=142,
                    model_used="gpt-4",
                ),
            ]
            db.add_all(messages)
            print(f"✓ Created sample conversation with {len(messages)} messages")

            # Commit all changes
            await db.commit()
            print("\n✅ Database seeding completed successfully!")
            print("\n📊 Summary:")
            print(f"   - {len(categories)} categories")
            print(f"   - {len(products)} products")
            print(f"   - {len(orders)} orders")
            print(f"   - {len(order_items)} order items")
            print(f"   - {len(stock_movements)} stock movements")
            print(f"   - {len(insights)} AI insights")
            print(f"   - 1 conversation with {len(messages)} messages")

        except Exception as e:
            await db.rollback()
            print(f"\n❌ Error seeding database: {str(e)}")
            raise


if __name__ == "__main__":
    print("🚀 WWS Inventory Platform - Database Seeding\n")
    asyncio.run(seed_database())
