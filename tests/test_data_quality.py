import pandas as pd
from src.data_quality import validate_data


def test_good_data_passes():
    df = pd.DataFrame({
        "order_id": [1, 2, 3, 4, 5],
        "customer_id": ["C001", "C002", "C003", "C004", "C005"],
        "quantity": [2, 1, 5, 3, 2],
        "price": [500, 1200, 200, 750, 400],
        "order_date": [
            "2026-09-23",
            "2026-09-23",
            "2026-09-23",
            "2026-09-23",
            "2026-09-23"
        ]
    })

    is_valid, errors = validate_data(df)

    assert is_valid is True
    assert errors == []


def test_negative_price_fails():
    df = pd.DataFrame({
        "order_id": [1, 2],
        "customer_id": ["C001", "C002"],
        "quantity": [2, 1],
        "price": [500, -1200],
        "order_date": ["2026-09-23", "2026-09-23"]
    })

    is_valid, errors = validate_data(df)

    assert is_valid is False
    assert "Price must be greater than 0" in errors


def test_null_value_fails():
    df = pd.DataFrame({
        "order_id": [1, 2],
        "customer_id": ["C001", None],
        "quantity": [2, 1],
        "price": [500, 1200],
        "order_date": ["2026-09-23", "2026-09-23"]
    })

    is_valid, errors = validate_data(df)

    assert is_valid is False
    assert "Unexpected null values in: customer_id" in errors


def test_stale_data_fails_freshness():
    df = pd.DataFrame({
        "order_id": [1, 2, 3, 4, 5],
        "customer_id": ["C001", "C002", "C003", "C004", "C005"],
        "quantity": [2, 1, 5, 3, 2],
        "price": [500, 1200, 200, 750, 400],
        "order_date": [
            "2020-01-01",
            "2020-01-01",
            "2020-01-01",
            "2020-01-01",
            "2020-01-01"
        ]
    })

    is_valid, errors = validate_data(df)

    assert is_valid is False
    assert any("Freshness SLA failed" in error for error in errors)


def test_abnormal_quantity_distribution_fails():
    df = pd.DataFrame({
        "order_id": [1, 2, 3, 4, 5],
        "customer_id": ["C001", "C002", "C003", "C004", "C005"],
        "quantity": [200, 200, 200, 200, 200],
        "price": [500, 500, 500, 500, 500],
        "order_date": [
            "2026-09-23",
            "2026-09-23",
            "2026-09-23",
            "2026-09-23",
            "2026-09-23"
        ]
    })

    is_valid, errors = validate_data(df)

    assert is_valid is False
    assert "Quantity distribution looks abnormal" in errors
