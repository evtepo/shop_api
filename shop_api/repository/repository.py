from abc import abstractmethod, ABC
from typing import TypeVar

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from models.product import Category, Product


Model = TypeVar("Model", Category, Product)


class BaseRepository(ABC):
    @abstractmethod
    async def create(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def get(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def get_one(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def update(self, **kwargs):
        raise NotImplementedError


class PostgresRepository(BaseRepository):
    async def create(self, model: Model, session: AsyncSession, data: dict) -> Model:
        instance = model(**data)
        session.add(instance)
        await session.commit()
        await session.refresh(instance)

        return instance

    async def delete(self, model: Model, session: AsyncSession, **filters) -> None:
        query = delete(model).filter_by(**filters)
        await session.execute(query)
        await session.commit()

    async def get(
        self,
        model: Model,
        session: AsyncSession,
        limit: int,
        offset: int,
        orders: tuple | None = None,
        **filters,
    ):
        query = select(model)

        if category_id := filters.get("category_id"):
            query = query.join(model.categories).filter(Category.id == category_id)
        else:
            query = query.filter_by(**filters)

        if orders:
            query = query.order_by(*orders)

        query = query.limit(limit).offset(offset)
        res = await session.execute(query)

        return res.scalars().all()

    async def get_one(self, model: Model, session: AsyncSession, **filters):
        query = select(model).filter_by(**filters)
        res = await session.execute(query)

        return res.scalar_one_or_none()

    async def update(self, model: Model, session: AsyncSession, data: dict, **filters):
        query = update(model).values(**data).filter_by(**filters)
        await session.execute(query)
        await session.commit()

        updated_instance = await self.get_one(model, session, **filters)

        return updated_instance


repository: BaseRepository | None = PostgresRepository()


async def get_repository():
    return repository
