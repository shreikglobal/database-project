import pandas as pd


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Remove duplicate orders
    df = df.drop_duplicates(subset=["order_id"])

    # Calculate total amount
    df["total_amount"] = df["quantity"] * df["price"]

    # Convert order date
    df["order_date"] = pd.to_datetime(df["order_date"])

    return df
