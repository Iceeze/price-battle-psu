def validate_matrix(matrix: list) -> bool:
    """
    Проверяет, что переданная матрица непустая, прямоугольная (или квадратная)
    и содержит исключительно числовые значения.
    """
    if not matrix or not isinstance(matrix, list):
        raise ValueError("Матрица не может быть пустой.")

    if not isinstance(matrix[0], list) or len(matrix[0]) == 0:
        raise ValueError("Матрица должна содержать хотя бы один элемент.")

    cols = len(matrix[0])
    for row in matrix:
        if not isinstance(row, list):
            raise ValueError("Матрица должна быть двумерным массивом.")
        if len(row) != cols:
            raise ValueError("Матрица должна быть строго прямоугольной или квадратной.")
        for item in row:
            if not isinstance(item, (int, float)):
                raise ValueError("Все элементы матрицы должны быть числами.")

    return True
