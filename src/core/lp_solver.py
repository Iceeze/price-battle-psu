import pulp


def optimize_price(cost: float, min_margin: float, max_price: float) -> dict:
    """Оптимизирует цену с помощью линейного программирования."""
    problem = pulp.LpProblem("PriceOptimization", pulp.LpMaximize)
    price = problem.add_variable("price", lowBound=cost, upBound=max_price)

    # Целевая функция
    problem += price - cost

    # Ограничения
    min_allowed_price = cost * (1 + min_margin / 100)
    problem += price >= min_allowed_price
    problem += price <= max_price

    # Решение без вывода логов в консоль
    problem.solve(pulp.COIN_CMD(msg=False))

    if pulp.LpStatus[problem.status] == "Optimal":
        optimal_p = pulp.value(price)
        return {
            "status": "optimal",
            "optimal_price": optimal_p,
            "profit_per_unit": optimal_p - cost,
            "margin_pct": ((optimal_p - cost) / cost) * 100,
        }

    return {
        "status": "infeasible",
        "optimal_price": 0.0,
        "profit_per_unit": 0.0,
        "margin_pct": 0.0,
    }
