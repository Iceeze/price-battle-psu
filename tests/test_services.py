from unittest.mock import patch
from src.models import MatrixGameRequest, PriceOptimizationRequest
from src.services.game_service import solve_game_service
from src.services.price_service import optimize_price_service


class TestGameService:
    def test_game_service_success_flow(self):
        request = MatrixGameRequest(matrix=[[10, 20], [15, 5]])

        response = solve_game_service(request)

        assert response.equilibrium_found is True
        assert response.seller_a_strategy is not None
        assert response.message == "Равновесие Нэша успешно рассчитано"

    def test_game_service_handles_solver_exception_negatively(self):
        request = MatrixGameRequest(matrix=[[1, 2], [3, 4]])

        with patch(
            "src.services.game_service.solve_nash_equilibrium",
            side_effect=RuntimeError("Сбой математического сопроцессора"),
        ):
            response = solve_game_service(request)

        assert response.equilibrium_found is False
        assert "Ошибка при решении игры" in response.message
        assert "Сбой математического сопроцессора" in response.message


class TestPriceService:
    def test_price_service_success_flow(self):
        request = PriceOptimizationRequest(cost=500, min_margin_pct=20, max_price=1000)

        response = optimize_price_service(request)

        assert response.status == "optimal"
        assert response.optimal_price == 1000.0
        assert response.message == "Оптимизация завершена успешно"

    def test_price_service_infeasible_business_scenario(self):
        request = PriceOptimizationRequest(cost=1000, min_margin_pct=50, max_price=1100)

        response = optimize_price_service(request)

        assert response.status == "infeasible"
        assert response.optimal_price == 0.0
        assert "Конфликт ограничений" in response.message

    def test_price_service_handles_solver_exception_negatively(self):
        request = PriceOptimizationRequest(cost=500, min_margin_pct=20, max_price=1000)

        with patch(
            "src.services.price_service.optimize_price",
            side_effect=Exception("PuLP solver crashed"),
        ):
            response = optimize_price_service(request)

        assert response.status == "error"
        assert "Ошибка при оптимизации" in response.message
        assert "PuLP solver crashed" in response.message
