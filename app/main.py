from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.auth.views import router as auth_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.include_router(auth_router, prefix="/api", tags=["auth"])

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.get("/")
def read_root() -> dict:
    return {"Name": "App API", "Description": "Welcome to Zombocom!"}
