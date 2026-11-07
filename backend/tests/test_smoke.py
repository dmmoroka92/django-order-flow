def test_basic_math() -> None:
    assert 2 + 2 == 4


def calculate_total(price: float, quantity: int) -> float:
    return price * quantity


def test_calculate_total() -> None:
    result = calculate_total(10.5, 2)

    assert result == 21.0
