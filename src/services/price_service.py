from src.core.lp_solver import optimize_price
from src.models import (
    PriceOptimizationRequest,
    PriceOptimizationResponse,
)


def optimize_price_service(
    request: PriceOptimizationRequest,
) -> PriceOptimizationResponse:
    try:
        result = optimize_price(request.cost, request.min_margin_pct, request.max_price)

        if result["status"] == "infeasible":
            msg = "Конфликт ограничений: невозможно достичь заданной маржи при такой максимальной цене"
        else:
            msg = "Оптимизация завершена успешно"

        return PriceOptimizationResponse(
            optimal_price=result["optimal_price"],
            profit_per_unit=result["profit_per_unit"],
            margin_pct=result["margin_pct"],
            status=result["status"],
            message=msg,
        )
    except Exception as e:
        return PriceOptimizationResponse(
            optimal_price=0.0,
            profit_per_unit=0.0,
            margin_pct=0.0,
            status="error",
            message=f"Ошибка при оптимизации: {str(e)}",
        )
