import pytest
from unittest.mock import patch

from src.main import run_cli
from src.models import MatrixGameResponse, PriceOptimizationResponse


def test_run_cli_file_not_found(capsys):
    with patch("builtins.open", side_effect=FileNotFoundError), patch(
        "sys.exit", side_effect=SystemExit
    ) as mock_exit:

        with pytest.raises(SystemExit):
            run_cli("dummy_path.yaml", "scenario_1")

        mock_exit.assert_called_once_with(1)
        captured = capsys.readouterr()
        assert "Ошибка: Файл конфигурации 'dummy_path.yaml' не найден." in captured.out


def test_run_cli_scenario_not_found(capsys):
    mock_config = {"other_scenario": {}}

    with patch("builtins.open"), patch(
        "yaml.safe_load", return_value=mock_config
    ), patch("sys.exit", side_effect=SystemExit) as mock_exit:

        with pytest.raises(SystemExit):
            run_cli("config.yaml", "missing_scenario")

        mock_exit.assert_called_once_with(1)
        captured = capsys.readouterr()
        assert "Ошибка: Сценарий 'missing_scenario' не найден." in captured.out
        assert "Доступные сценарии: other_scenario" in captured.out


@patch("src.main.optimize_price_service")
@patch("src.main.solve_game_service")
def test_run_cli_success_flow(mock_solve_game, mock_optimize_price, capsys):
    mock_config = {
        "test_scenario": {
            "game": {"description": "Тестовая игра", "matrix": [[1, 2], [3, 4]]},
            "optimization": {"cost": 100, "min_margin_pct": 10, "max_price": 200},
        }
    }

    mock_solve_game.return_value = MatrixGameResponse(
        equilibrium_found=True,
        seller_a_strategy=[1.0, 0.0],
        seller_b_strategy=[0.0, 1.0],
        expected_profit=50.5,
        message="Успех",
    )
    mock_optimize_price.return_value = PriceOptimizationResponse(
        optimal_price=150.0,
        profit_per_unit=50.0,
        margin_pct=50.0,
        status="optimal",
        message="Оптимизировано",
    )

    with patch("builtins.open"), patch("yaml.safe_load", return_value=mock_config):

        run_cli("config.yaml", "test_scenario")

        captured = capsys.readouterr()
        assert "Сценарий: Тестовая игра" in captured.out
        assert "Равновесие найдено: True" in captured.out
        assert "Ожидаемая прибыль: 50.50" in captured.out
        assert "Статус солвера: OPTIMAL" in captured.out
        assert "Оптимальная цена: 150.0" in captured.out


@patch("src.main.optimize_price_service")
@patch("src.main.solve_game_service")
def test_run_cli_handles_service_exceptions(
    mock_solve_game, mock_optimize_price, capsys
):
    mock_config = {
        "test_scenario": {
            "game": {"matrix": [[1, 2], [3, 4]]},
            "optimization": {"cost": 10, "min_margin_pct": 10, "max_price": 50},
        }
    }

    mock_solve_game.side_effect = Exception("Сломалась матрица")
    mock_optimize_price.side_effect = Exception("Сломался солвер")

    with patch("builtins.open"), patch("yaml.safe_load", return_value=mock_config):

        run_cli("config.yaml", "test_scenario")

        captured = capsys.readouterr()
        assert "Ошибка матрицы: Сломалась матрица" in captured.out
        assert "Ошибка оптимизации: Сломался солвер" in captured.out
