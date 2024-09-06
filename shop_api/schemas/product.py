from uuid import UUID

from pydantic import BaseModel, conint


class ProductMixin(BaseModel):
    title: str
    price: float
    rating: conint(ge=1, le=10)
    description: str | None


class CategoryMixin(BaseModel):
    title: str


class CreateCategory(CategoryMixin): ...


class GetCategory(CategoryMixin):
    id: UUID
    products: list[ProductMixin | None] = []

    class Config:
        from_attributes = True


class CreateProduct(ProductMixin):
    categories: list[UUID]


class DeleteProduct(BaseModel):
    id: UUID


class GetProduct(ProductMixin):
    id: UUID
    categories: list[CategoryMixin | None] = []

    class Config:
        from_attributes = True


class UpdateProduct(ProductMixin):
    id: UUID
    categories: list[UUID]
