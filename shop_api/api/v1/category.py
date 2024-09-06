from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.db_connect import get_session
from models.product import Category
from repository.repository import BaseRepository, get_repository
from schemas.product import CreateCategory, GetCategory
from services.category import get_all_categories, new_category


session_dependency = Annotated[AsyncSession, Depends(get_session)]
repository_dependency = Annotated[BaseRepository, Depends(get_repository)]

router = APIRouter(prefix="/api/v1/category")


@router.post("/", response_model=GetCategory | None, status_code=status.HTTP_201_CREATED)
async def create_category(
    category: CreateCategory,
    repository: repository_dependency,
    session: session_dependency,
):
    return await new_category(repository, Category, category, session)


@router.get("/", response_model=dict[str, list[GetCategory] | dict], status_code=status.HTTP_200_OK)
async def get_categories(
    repository: repository_dependency,
    session: session_dependency,
    page: int = Query(default=1, ge=1, description="Page number"),
    size: int = Query(default=10, ge=10, le=50, description="Page size"),
):
    return await get_all_categories(repository, Category, session, page, size)
