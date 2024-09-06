import uvicorn
from fastapi import FastAPI

from api.v1.category import router as category_router
from api.v1.product import router as product_router
from config.settings import settings


app = FastAPI()

app.include_router(category_router, tags=["Category"])
app.include_router(product_router, tags=["Product"])


if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host=settings.local_host,
        port=settings.local_port,
    )
