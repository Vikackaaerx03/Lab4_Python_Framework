from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.database import Base, engine
from app.router.order import router as order_router
from app.router.web import router as web_router

app = FastAPI(
    title="Lab 4 Order REST API",
    description="REST API and web interface for managing orders",
    version="1.0.0",
)

Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(web_router)
app.include_router(order_router)


@app.get("/test")
def test():
    return {"message": "App is working"}
