"""
Product model
"""
from sqlalchemy import Column, String, Float, Integer, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class Product(BaseModel):
    """
    Product model representing inventory items
    """

    __tablename__ = "products"

    # Basic information
    name = Column(String(255), nullable=False, index=True)
    sku = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    category = Column(String(100), nullable=True, index=True)

    # Pricing
    cost_price = Column(Float, nullable=False, default=0.0)
    selling_price = Column(Float, nullable=False, default=0.0)
    currency = Column(String(3), default="EUR")

    # Inventory
    stock_quantity = Column(Integer, nullable=False, default=0)
    reorder_point = Column(Integer, nullable=True)
    reorder_quantity = Column(Integer, nullable=True)
    warehouse_location = Column(String(100), nullable=True)

    # Tracking
    is_active = Column(Boolean, default=True)
    barcode = Column(String(100), nullable=True, unique=True)
    image_url = Column(String(500), nullable=True)

    # Relationships
    # order_items = relationship("OrderItem", back_populates="product")

    def __repr__(self) -> str:
        return f"<Product(id={self.id}, sku={self.sku}, name={self.name})>"


class ProductCategory(BaseModel):
    """
    Product category model
    """

    __tablename__ = "product_categories"

    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    parent_id = Column(Integer, ForeignKey("product_categories.id"), nullable=True)

    # Self-referential relationship for nested categories
    parent = relationship("ProductCategory", remote_side="ProductCategory.id", backref="children")

    def __repr__(self) -> str:
        return f"<ProductCategory(id={self.id}, name={self.name})>"


class StockMovement(BaseModel):
    """
    Stock movement tracking model
    """

    __tablename__ = "stock_movements"

    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    movement_type = Column(String(50), nullable=False)  # in, out, adjustment, transfer
    quantity = Column(Integer, nullable=False)
    reference_type = Column(String(50), nullable=True)  # order, return, adjustment
    reference_id = Column(Integer, nullable=True)
    notes = Column(Text, nullable=True)
    performed_by = Column(String(100), nullable=True)

    # Relationship
    product = relationship("Product")

    def __repr__(self) -> str:
        return f"<StockMovement(id={self.id}, product_id={self.product_id}, type={self.movement_type})>"
