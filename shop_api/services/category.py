from sqlalchemy.ext.asyncio import AsyncSession

from models.product import Category
from repository.repository import BaseRepository
from schemas.product import CreateCategory


async def new_category(
    repository: BaseRepository,
    model: Category,
    category: CreateCategory,
    session: AsyncSession,
):
    return await repository.create(model, session, category.model_dump())


async def get_all_categories(
    repository: BaseRepository,
    model: Category,
    session: AsyncSession,
    page: int,
    size: int,
):
    prev_page = page - 1 if page - 1 > 0 else None
    next_page = page
    page = (page - 1) * size

    data = await repository.get(model, session, size, page)

    next_page = next_page + 1 if data and len(data) == size else None

    result = {
        "links": {
            "prev": prev_page,
            "next": next_page,
        },
    }
    result["data"] = data

    return result
