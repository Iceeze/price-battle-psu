from fastapi import FastAPI

from src.api.routes import router


def create_app() -> FastAPI:
    """Создает экземпляр FastAPI приложения."""
    app = FastAPI(
        title="Price Battle API",
        description="Симулятор конкурентного ценообразования на основе теории игр и линейного программирования.",
        version="1.0.0",
    )
    app.include_router(router)

    return app
