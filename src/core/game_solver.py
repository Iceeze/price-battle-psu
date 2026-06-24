import numpy as np
import nashpy as nash


def solve_nash_equilibrium(
    matrix_a: list[list[float]],
) -> list[tuple[list[float], list[float]]]:
    """
    Функция для вычисления равновесия Нэша.
    Использует метод перебора носителей.
    """
    A = np.array(matrix_a)
    B = -A
    game = nash.Game(A, B)
    equilibria = list(game.support_enumeration())

    result = []
    for eq in equilibria:
        result.append((eq[0].tolist(), eq[1].tolist()))

    return result
