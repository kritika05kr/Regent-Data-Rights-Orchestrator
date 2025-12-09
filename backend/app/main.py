from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import requests as requests_router
from app.api.routes import admin as admin_router
from app.core.config import get_settings
from app.db.base_class import Base
from app.db.session import engine

settings = get_settings()

# 🔹 Create all tables at startup (VERY IMPORTANT)
Base.metadata.create_all(bind=engine)


def get_application() -> FastAPI:
    app = FastAPI(
        title="Regent Data Rights Orchestrator",
        version="1.0.0",
        description="Automating GDPR/CCPA data rights workflows",
    )

    # 🔹 CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.FRONTEND_ORIGIN],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 🔹 Routers – no prefix to avoid the '/' assertion error
    app.include_router(requests_router.router)
    app.include_router(admin_router.router)

    return app


app = get_application()
