import argparse
import sys
import yaml
import uvicorn

from src.models import MatrixGameRequest, PriceOptimizationRequest
from src.services import solve_game_service, optimize_price_service
from src.api.app import create_app

app = create_app()


def run_cli(config_path: str, scenario_name: str):
    """Скрипт для запуска расчетов через консоль на основе YAML-конфигурации."""
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Ошибка: Файл конфигурации '{config_path}' не найден.")
        sys.exit(1)

    if scenario_name not in config:
        print(f"Ошибка: Сценарий '{scenario_name}' не найден.")
        print(f"Доступные сценарии: {', '.join(config.keys())}")
        sys.exit(1)

    scenario_data = config[scenario_name]

    # Извлекаем вложенные словари из конфига
    game_data = scenario_data.get("game", {})
    opt_data = scenario_data.get("optimization", {})
    description = game_data.get("description", "Без описания")

    print("=" * 60)
    print(f"Сценарий: {description}")
    print("=" * 60)

    # --- БЛОК 1: ТЕОРИЯ ИГР ---
    print("\n[1] Поиск равновесия Нэша")
    try:
        matrix_req = MatrixGameRequest(matrix=game_data.get("matrix", []))
        game_res = solve_game_service(matrix_req)

        print(f"• Равновесие найдено: {game_res.equilibrium_found}")
        if game_res.equilibrium_found:
            print(f"• Стратегия A: {game_res.seller_a_strategy}")
            print(f"• Стратегия B: {game_res.seller_b_strategy}")
            print(f"• Ожидаемая прибыль: {game_res.expected_profit:.2f}")
        else:
            print(f"• Сообщение: {game_res.message}")

    except Exception as e:
        print(f"Ошибка матрицы: {e}")

    # --- БЛОК 2: ЛИНЕЙНОЕ ПРОГРАММИРОВАНИЕ ---
    print("\n[2] Оптимизация цены (ЛП)")
    try:
        opt_req = PriceOptimizationRequest(**opt_data)
        opt_res = optimize_price_service(opt_req)

        print(f"• Статус солвера: {opt_res.status.upper()}")
        print(f"• Оптимальная цена: {opt_res.optimal_price}")
        print(f"• Прибыль с единицы: {opt_res.profit_per_unit}")
        print(f"• Фактическая маржа: {opt_res.margin_pct:.2f} %")
        print(f"• Детали: {opt_res.message}")

    except Exception as e:
        print(f"Ошибка оптимизации: {e}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="PriceBattle: Инструмент конкурентного ценообразования"
    )

    # Флаг для запуска FastAPI сервера
    parser.add_argument(
        "--api", action="store_true", help="Запустить REST API сервер на порту 8000"
    )

    # Флаги для консольного запуска сценариев
    parser.add_argument(
        "--config",
        type=str,
        help="Путь к YAML файлу конфигурации (например, config/scenario.yaml)",
    )
    parser.add_argument(
        "--scenario",
        type=str,
        help="Название сценария для запуска (например, typical)",
    )

    args = parser.parse_args()

    if args.api:
        print("🚀 Запуск FastAPI сервера...")
        uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)

    elif args.config and args.scenario:
        run_cli(args.config, args.scenario)
