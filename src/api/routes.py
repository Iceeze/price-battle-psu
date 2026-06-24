from fastapi import APIRouter

from src.models import (
    MatrixGameRequest,
    MatrixGameResponse,
    PriceOptimizationRequest,
    PriceOptimizationResponse,
)
from src.services.game_service import solve_game_service
from src.services.price_service import optimize_price_service

router = APIRouter()


@router.get("/health", summary="Проверка доступности сервиса")
def health_check():
    return {"status": "ok"}


@router.get("/example_data", summary="Получить пример данных для тестирования")
def get_example_data():
    return {
        "matrix_example": [[12, 18], [25, 8]],
        "optimization_example": {"cost": 500, "min_margin_pct": 30, "max_price": 1200},
    }


@router.post(
    "/equilibrium", response_model=MatrixGameResponse, summary="Найти равновесие Нэша"
)
def find_nash_equilibrium(request: MatrixGameRequest):
    return solve_game_service(request)


@router.post(
    "/optimize",
    response_model=PriceOptimizationResponse,
    summary="Оптимизировать цену (ЛП)",
)
def optimize_margin_price(request: PriceOptimizationRequest):
    return optimize_price_service(request)
