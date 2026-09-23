import pandas as pd


def validate_data(df: pd.DataFrame):
    errors = []

    required_columns = [
        "order_id",
        "customer_id",
        "quantity",
        "price",
        "order_date"
    ]

    missing_columns = [
        col for col in required_columns if col not in df.columns
    ]

    if missing_columns:
        errors.append(f"Missing columns: {missing_columns}")

    if errors:
        return False, errors

    # Row count
    if not 5 <= len(df) <= 1000:
        errors.append(
            f"Invalid row count: {len(df)}. Expected between 5 and 1000."
        )

    # Null check
    for col in required_columns:
        if df[col].isnull().any():
            errors.append(f"Unexpected null values in: {col}")

    # Valid values
    if (df["quantity"] <= 0).any():
        errors.append("Quantity must be greater than 0")

    if (df["price"] <= 0).any():
        errors.append("Price must be greater than 0")

    # Duplicate IDs
    if df["order_id"].duplicated().any():
        errors.append("Duplicate order_id found")

    # Date validation
    parsed_dates = pd.to_datetime(df["order_date"], errors="coerce")

    if parsed_dates.isnull().any():
        errors.append("Invalid order_date found")

    # Freshness: latest record should be within 48 hours
    latest_date = parsed_dates.max()
    age_hours = (pd.Timestamp.now() - latest_date).total_seconds() / 3600

    if age_hours > 48:
        errors.append(
            f"Freshness SLA failed: latest data is {age_hours:.1f} hours old"
        )

    # Distribution sanity
    if df["quantity"].mean() > 100:
        errors.append("Quantity distribution looks abnormal")

    if df["price"].mean() > 100000:
        errors.append("Price distribution looks abnormal")

    return len(errors) == 0, errors
