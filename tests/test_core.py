import pytest

from src.core.game_solver import solve_nash_equilibrium
from src.core.lp_solver import optimize_price


class TestGameSolver:
    def test_solve_nash_equilibrium_with_mixed_strategy(self):
        matrix = [[1, -1], [-1, 1]]

        equilibria = solve_nash_equilibrium(matrix)

        assert len(equilibria) > 0

        strategy_a, strategy_b = equilibria[0]

        assert strategy_a == pytest.approx([0.5, 0.5])
        assert strategy_b == pytest.approx([0.5, 0.5])

    def test_solve_nash_equilibrium_with_saddle_point(self):
        matrix = [[3, 1], [2, 0]]

        equilibria = solve_nash_equilibrium(matrix)

        assert len(equilibria) > 0
        strategy_a, strategy_b = equilibria[0]

        assert strategy_a == pytest.approx([1.0, 0.0])
        assert strategy_b == pytest.approx([0.0, 1.0])

    def test_solve_nash_equilibrium_with_empty_matrix_raises_error(self):
        invalid_matrix = []

        with pytest.raises((ValueError, IndexError)):
            solve_nash_equilibrium(invalid_matrix)


class TestLPSolver:
    def test_optimize_price_returns_optimal(self):
        cost = 800.0
        min_margin = 20.0
        max_price = 1500.0

        result = optimize_price(cost, min_margin, max_price)

        assert result["status"] == "optimal"
        assert result["optimal_price"] == 1500.0
        assert result["profit_per_unit"] == 700.0

    def test_optimize_price_returns_infeasible_on_conflict(self):
        cost = 1000.0
        min_margin = 50.0
        max_price = 1200.0

        result = optimize_price(cost, min_margin, max_price)

        assert result["status"] == "infeasible"
        assert result["optimal_price"] == 0.0
        assert result["profit_per_unit"] == 0.0

    def test_optimize_price_with_invalid_types_raises_error(self):
        invalid_cost = "строка_вместо_числа"

        with pytest.raises(TypeError):
            optimize_price(invalid_cost, 20.0, 1200.0)
