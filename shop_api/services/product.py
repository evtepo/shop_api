from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import asc, desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.product import Category, Product
from repository.repository import BaseRepository
from schemas.product import CreateProduct, DeleteProduct, UpdateProduct


async def new_product(
    model: Product,
    product: CreateProduct,
    session: AsyncSession,
    repository: BaseRepository,
):
    data = product.model_dump()
    category_ids = data.pop("categories", [])

    instance = await repository.create(model, session, data)
    if category_ids:
        query = select(Category).filter(Category.id.in_(category_ids))
        categories = await session.execute(query)

        instance.categories = categories.scalars().all()

        await session.commit()
        await session.refresh(instance)

    return instance


async def delete_product_by_id(
    model: Product,
    product: DeleteProduct,
    session: AsyncSession,
    repository: BaseRepository,
):
    await repository.delete(model, session, **product.model_dump())

    return {"msg": "Successfully deleted."}


async def get_all_products(
    model: Product,
    session: AsyncSession,
    repository: BaseRepository,
    page: int,
    size: int,
    orders: dict,
    filters: dict,
):
    order_by = tuple()

    if order_by_price := orders.get("price"):
        if order_by_price.startswith("-"):
            order_by += (desc(model.price),)
        else:
            order_by += (asc(model.price),)

    if order_by_rating := orders.get("rating"):
        if order_by_rating.startswith("-"):
            order_by += (desc(model.rating),)
        else:
            order_by += (asc(model.rating),)

    prev_page = page - 1 if page - 1 > 0 else None
    next_page = page
    page = (page - 1) * size

    data = await repository.get(model, session, size, page, order_by, **filters)

    next_page = next_page + 1 if data and len(data) == size else None

    result = {
        "links": {
            "prev": prev_page,
            "next": next_page,
        },
    }
    result["data"] = data

    return result


async def get_one_product(
    model: Product,
    product_id: UUID,
    session: AsyncSession,
    repository: BaseRepository,
):
    return await repository.get_one(model, session, id=product_id)


async def update_product_by_id(
    model: Product,
    product: UpdateProduct,
    session: AsyncSession,
    repository: BaseRepository,
):
    data = product.model_dump()
    category_ids = data.pop("categories", [])

    instance = await repository.update(model, session, data, id=product.id)
    if instance is None:
        raise HTTPException(status_code=404, detail="Product not found")

    if category_ids:
        query = select(Category).filter(Category.id.in_(category_ids))
        result = await session.execute(query)
        categories = result.scalars().all()

        instance.categories = categories

        await session.commit()
        await session.refresh(instance)

    return instance
