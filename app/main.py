from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.core.constants import APP_NAME
from app.core.exceptions import AppError
from app.db.database import close_client, init_db
from app.routers.auth_router import router as auth_router
from app.routers.lookup_router import router as lookup_router
from app.routers.user_router import router as user_router

app = FastAPI(
    title=APP_NAME,
    description="REST API for IP geolocation, authentication, and MongoDB lookup history",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(lookup_router)
app.mount("/frontend", StaticFiles(directory="frontend", html=True), name="frontend")


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.on_event("shutdown")
def shutdown() -> None:
    close_client()


@app.exception_handler(AppError)
async def handle_app_error(_: Request, exc: AppError):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.get("/")
def root():
    return RedirectResponse("/frontend/index.html")
