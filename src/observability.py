from datetime import datetime
import csv
import os


RUN_LOG = "data/monitoring/run_history.csv"


def record_run(
    status,
    start_time,
    end_time,
    input_rows,
    output_rows,
    quality_status,
    freshness_status,
    sla_status,
    failed_stage="",
    error_message="",
    downstream_impact=""
):
    duration_seconds = round(
        (end_time - start_time).total_seconds(), 2
    )

    record = {
        "run_timestamp": start_time.isoformat(),
        "status": status,
        "duration_seconds": duration_seconds,
        "input_rows": input_rows,
        "output_rows": output_rows,
        "quality_status": quality_status,
        "freshness_status": freshness_status,
        "sla_status": sla_status,
        "failed_stage": failed_stage,
        "error_message": error_message,
        "downstream_impact": downstream_impact,
    }

    os.makedirs(os.path.dirname(RUN_LOG), exist_ok=True)

    file_exists = os.path.exists(RUN_LOG)

    with open(RUN_LOG, "a", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=record.keys()
        )

        if not file_exists:
            writer.writeheader()

        writer.writerow(record)
