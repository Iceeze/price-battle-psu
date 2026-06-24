import numpy as np

from src.core.game_solver import solve_nash_equilibrium
from src.models import (
    MatrixGameRequest,
    MatrixGameResponse,
)


def solve_game_service(request: MatrixGameRequest) -> MatrixGameResponse:
    try:
        equilibria = solve_nash_equilibrium(request.matrix)

        if not equilibria:
            return MatrixGameResponse(
                equilibrium_found=False,
                message="Равновесие не найдено для переданной матрицы",
            )

        seller_a, seller_b = equilibria[0]
        A = np.array(request.matrix)
        expected_profit = float(np.dot(np.dot(seller_a, A), seller_b))

        return MatrixGameResponse(
            equilibrium_found=True,
            seller_a_strategy=seller_a,
            seller_b_strategy=seller_b,
            expected_profit=expected_profit,
            message="Равновесие Нэша успешно рассчитано",
        )
    except Exception as e:
        return MatrixGameResponse(
            equilibrium_found=False,
            message=f"Ошибка при решении игры: {str(e)}",
        )
