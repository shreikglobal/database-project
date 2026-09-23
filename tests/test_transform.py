import pandas as pd

from src.transform import transform_data


def test_total_amount_calculation():
    df = pd.DataFrame({
        "order_id": [1],
        "customer_id": ["C001"],
        "quantity": [2],
        "price": [500],
        "order_date": ["2026-09-23"]
    })

    result = transform_data(df)

    assert result.iloc[0]["total_amount"] == 1000


def test_duplicate_orders_removed():
    df = pd.DataFrame({
        "order_id": [1, 1],
        "customer_id": ["C001", "C001"],
        "quantity": [2, 2],
        "price": [500, 500],
        "order_date": ["2026-09-23", "2026-09-23"]
    })

    result = transform_data(df)

    assert len(result) == 1
