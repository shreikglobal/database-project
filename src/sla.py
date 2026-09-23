from datetime import datetime
import pandas as pd


FRESHNESS_TARGET_HOURS = 48


def calculate_sla_status(df, quality_passed):
    latest_date = pd.to_datetime(df["order_date"], errors="coerce").max()

    freshness_hours = (
        (pd.Timestamp.now() - latest_date).total_seconds() / 3600
    )

    freshness_status = freshness_hours <= FRESHNESS_TARGET_HOURS

    completeness_status = not df[
        ["order_id", "customer_id", "quantity", "price", "order_date"]
    ].isnull().any().any()

    quality_status = quality_passed

    overall_status = (
        freshness_status
        and completeness_status
        and quality_status
    )

    return {
        "run_timestamp": datetime.now().isoformat(),
        "freshness_hours": round(freshness_hours, 2),
        "freshness_status": "PASS" if freshness_status else "FAIL",
        "completeness_status": "PASS" if completeness_status else "FAIL",
        "quality_status": "PASS" if quality_status else "FAIL",
        "overall_status": "PASS" if overall_status else "FAIL",
    }
