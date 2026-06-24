from pydantic import BaseModel, Field, field_validator
from src.utils import validate_matrix

# --- Request Models ---


class MatrixGameRequest(BaseModel):
    matrix: list[list[float]] = Field(..., title="Платежная матрица A")

    @field_validator("matrix")
    @classmethod
    def check_matrix(cls, v):
        validate_matrix(v)
        return v


class PriceOptimizationRequest(BaseModel):
    cost: float = Field(..., gt=0, description="Себестоимость")
    min_margin_pct: float = Field(..., ge=0, description="Минимальная маржа (%)")
    max_price: float = Field(..., gt=0, description="Максимальная цена")


# --- Response Models ---


class MatrixGameResponse(BaseModel):
    equilibrium_found: bool = Field(
        description="Указывает, было ли найдено равновесие Нэша"
    )
    seller_a_strategy: list[float] | None = Field(
        default=None, description="Вектор вероятностей для продавца А"
    )
    seller_b_strategy: list[float] | None = Field(
        default=None, description="Вектор вероятностей для продавца Б"
    )
    expected_profit: float | None = Field(
        default=None, description="Математическое ожидание прибыли"
    )
    message: str = Field(default="Успешно", description="Статус операции")


class PriceOptimizationResponse(BaseModel):
    optimal_price: float = Field(description="Итоговая рекомендуемая цена")
    profit_per_unit: float = Field(description="Абсолютная прибыль с одной единицы")
    margin_pct: float = Field(description="Фактическая маржинальность в процентах")
    status: str = Field(
        default="optimal", description="Статус решения линейного программирования"
    )
    message: str = Field(
        default="Оптимизация завершена успешно",
        description="Детальное сообщение от солвера",
    )
