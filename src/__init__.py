from fastapi import FastAPI
from src.books.routes import book_router
from contextlib import asynccontextmanager

@asynccontextmanager
async def life_span(app: FastAPI):
    # ✅ Start-up logic here
    print("Server is starting ...")
    yield
    # ✅ Shut-down logic here
    print("Server has been stopped")

version = 'v1'

app = FastAPI(
    title= "Bookely",
    description= "REST API for a book review web service",
    version= version,
    lifespan=life_span
)

app.include_router(book_router, prefix=f"/api/{version}/books", tags=['Books'])