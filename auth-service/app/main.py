from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.settings import settings
from app.di import Container
from app.adapters.http.health_router import router as health_router
from app.adapters.http.auth_router import router as auth_router


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        description="Authentication & Authorization Service",
        version="1.0.0",
        swagger_ui_parameters={"persistAuthorization": True}
    )
    app.container = Container()  # type: ignore[attr-defined]

    # CORS
    origins = [o.strip() for o in settings.CORS_ORIGINS.split(",") if o.strip()]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Routers
    app.include_router(health_router)
    app.include_router(auth_router, prefix="/auth", tags=["Authentication"])

    return app