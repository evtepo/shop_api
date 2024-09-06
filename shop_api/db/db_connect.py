from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from config.settings import postgres_dsn


Base = declarative_base()

engine = create_async_engine(postgres_dsn)
async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=True)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        session: AsyncSession
        try:
            yield session
        except Exception:
            await session.rollback()
        finally:
            await session.close()
