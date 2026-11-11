from fastapi import FastAPI
from database import create_tables
from routes.users import router as user_router
from routes.books import router as book_router

ver = "v1"
app = FastAPI(
    title="Kitab Exchange API", description="An API for exchanging books", version=ver
)


@app.on_event("startup")
def on_startup():
    create_tables()


@app.get("/")
def index():
    return {"message": "Welcome to the Kitab Exchange API!"}


app.include_router(user_router, prefix="/api/{ver}/user", tags=["User"])
app.include_router(book_router, prefix="/api/{ver}/book", tags=["Book"])
