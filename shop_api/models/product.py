from uuid import UUID

from sqlalchemy import ForeignKey, Integer, Numeric, String, Text 
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from db.db_connect import Base
from models.base import BaseMixin


class Category(Base, BaseMixin):
    title: Mapped[str] = mapped_column()

    products: Mapped[list["Product"]] = relationship(
        "Product",
        secondary="product_category",
        back_populates="categories",
        lazy="selectin",
    )


class Product(Base, BaseMixin):
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[float] = mapped_column(Numeric(precision=10, scale=2))
    rating: Mapped[int] = mapped_column(Integer)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    categories: Mapped[list["Category"]] = relationship(
        "Category",
        secondary="product_category",
        back_populates="products",
        lazy="selectin",
    )

    @validates("rating")
    def validate_rating(self, key, value):
        if value < 1 or value > 10:
            raise ValueError("Rating must be between 1 and 10")
        
        return value


class ProductCategory(Base):
    __tablename__ = "product_category"

    category_id: Mapped[UUID] = mapped_column(ForeignKey("category.id", ondelete="CASCADE"), primary_key=True)
    product_id: Mapped[UUID] = mapped_column(ForeignKey("product.id", ondelete="CASCADE"), primary_key=True)
