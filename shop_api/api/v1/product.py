from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.db_connect import get_session
from models.product import Product
from repository.repository import BaseRepository, get_repository
from schemas.product import CreateProduct, DeleteProduct, GetProduct, UpdateProduct
from services import product as product_logic


session_dependency = Annotated[AsyncSession, Depends(get_session)]
repository_dependency = Annotated[BaseRepository, Depends(get_repository)]

router = APIRouter(prefix="/api/v1/product")


@router.post("/", response_model=GetProduct | dict, status_code=status.HTTP_201_CREATED)
async def create_product(
    product: CreateProduct,
    session: session_dependency,
    repository: repository_dependency,
):
    return await product_logic.new_product(Product, product, session, repository)


@router.delete("/", response_model=dict[str, str], status_code=status.HTTP_200_OK)
async def delete_product(
    product: DeleteProduct,
    session: session_dependency,
    repository: repository_dependency,
):
    return await product_logic.delete_product_by_id(Product, product, session, repository)


@router.get(
    "/",
    response_model=dict[str, list[GetProduct] | dict],
    status_code=status.HTTP_200_OK,
)
async def get_products(
    session: session_dependency,
    repository: repository_dependency,
    page: int = Query(default=1, ge=1, description="Page number"),
    size: int = Query(default=10, ge=10, le=50, description="Page size"),
    sort_by_category: UUID | None = Query(
        default=None,
        description="Sort by category, use 'category_id' (3fa85f64-5717-4562-b3fc-2c963f66afa6)",
    ),
    order_by_price: str | None = Query(
        default=None,
        description="Order by price, use 'price' for ascending or '-price' for descending order",
    ),
    order_by_rating: str | None = Query(
        default=None,
        description="Order by rating, use 'rating' for ascending or '-rating' for descending order",
    ),
):
    filters = {"category_id": sort_by_category} if sort_by_category else {}
    order_py = {"price": order_by_price, "rating": order_by_rating}

    return await product_logic.get_all_products(Product, session, repository, page, size, order_py, filters)


@router.get(
    "/{product_id}",
    response_model=GetProduct | None,
    status_code=status.HTTP_200_OK,
)
async def get_product(
    product_id: UUID,
    session: session_dependency,
    repository: repository_dependency,
):
    return await product_logic.get_one_product(Product, product_id, session, repository)


@router.put(
    "/",
    response_model=GetProduct | None,
    status_code=status.HTTP_200_OK,
)
async def update_product(
    product: UpdateProduct,
    session: session_dependency,
    repository: repository_dependency,
):
    return await product_logic.update_product_by_id(Product, product, session, repository)
