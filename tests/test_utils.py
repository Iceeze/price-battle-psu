import pytest
from src.utils import validate_matrix


def test_validate_matrix_returns_true_for_valid_matrix():
    valid_matrix = [[1.0, 2.5, 3], [4, 5.5, 6]]

    result = validate_matrix(valid_matrix)

    assert result is True


def test_validate_matrix_raises_error_for_empty_matrix():
    empty_matrix = []

    with pytest.raises(ValueError, match="Матрица не может быть пустой"):
        validate_matrix(empty_matrix)


def test_validate_matrix_raises_error_for_flat_list():
    flat_matrix = [1, 2, 3]

    with pytest.raises(
        ValueError, match="Матрица должна содержать хотя бы один элемент"
    ):
        validate_matrix(flat_matrix)


def test_validate_matrix_raises_error_for_jagged_matrix():
    jagged_matrix = [[1, 2, 3], [4, 5]]  # Здесь не хватает элемента

    with pytest.raises(
        ValueError, match="Матрица должна быть строго прямоугольной или квадратной"
    ):
        validate_matrix(jagged_matrix)


def test_validate_matrix_raises_error_for_invalid_types():
    invalid_type_matrix = [[1, 2], [3, "четыре"]]  # Ошибка типа

    with pytest.raises(ValueError, match="Все элементы матрицы должны быть числами"):
        validate_matrix(invalid_type_matrix)
