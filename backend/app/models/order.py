"""
Order models
"""
from sqlalchemy import Column, String, Float, Integer, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
import enum

from app.models.base import BaseModel


class OrderStatus(str, enum.Enum):
    """Order status enumeration"""

    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class Order(BaseModel):
    """
    Order model
    """

    __tablename__ = "orders"

    # Order information
    order_number = Column(String(50), unique=True, nullable=False, index=True)
    status = Column(SQLEnum(OrderStatus), default=OrderStatus.PENDING, nullable=False, index=True)

    # Customer information
    customer_name = Column(String(255), nullable=False)
    customer_email = Column(String(255), nullable=True)
    customer_phone = Column(String(50), nullable=True)

    # Shipping address
    shipping_address_line1 = Column(String(255), nullable=True)
    shipping_address_line2 = Column(String(255), nullable=True)
    shipping_city = Column(String(100), nullable=True)
    shipping_state = Column(String(100), nullable=True)
    shipping_postal_code = Column(String(20), nullable=True)
    shipping_country = Column(String(100), nullable=True)

    # Financial
    subtotal = Column(Float, nullable=False, default=0.0)
    tax = Column(Float, nullable=False, default=0.0)
    shipping_cost = Column(Float, nullable=False, default=0.0)
    total_amount = Column(Float, nullable=False, default=0.0)
    currency = Column(String(3), default="EUR")

    # Additional information
    notes = Column(Text, nullable=True)
    tracking_number = Column(String(100), nullable=True)

    # Relationships
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Order(id={self.id}, order_number={self.order_number}, status={self.status})>"


class OrderItem(BaseModel):
    """
    Order item model (line items in an order)
    """

    __tablename__ = "order_items"

    # Order reference
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, index=True)

    # Product reference
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)

    # Item details
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    discount = Column(Float, nullable=False, default=0.0)
    subtotal = Column(Float, nullable=False)

    # Product snapshot (in case product details change)
    product_name = Column(String(255), nullable=False)
    product_sku = Column(String(100), nullable=False)

    # Relationships
    order = relationship("Order", back_populates="items")
    product = relationship("Product")

    def __repr__(self) -> str:
        return f"<OrderItem(id={self.id}, order_id={self.order_id}, product_id={self.product_id})>"
