from extract import extract_data
from transform import transform_data
from data_quality import validate_data
from sla import calculate_sla_status
from observability import record_run

import csv
import os
from datetime import datetime


INPUT_FILE = "data/input/orders.csv"
OUTPUT_FILE = "data/output/processed_orders.csv"
SLA_FILE = "data/monitoring/sla_history.csv"


def save_sla_status(sla_status):
    os.makedirs(os.path.dirname(SLA_FILE), exist_ok=True)

    file_exists = os.path.exists(SLA_FILE)

    with open(SLA_FILE, "a", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=sla_status.keys()
        )

        if not file_exists:
            writer.writeheader()

        writer.writerow(sla_status)


def run_pipeline():
    start_time = datetime.now()

    input_rows = 0
    output_rows = 0

    try:
        print("Starting pipeline...")

        # Extract
        df = extract_data(INPUT_FILE)
        input_rows = len(df)
        print(f"Input rows: {input_rows}")
        # Row-count anomaly detection
        if os.path.exists("data/monitoring/run_history.csv"):
            with open("data/monitoring/run_history.csv", newline="") as file:
                rows = list(csv.DictReader(file))

            if rows:
                previous_rows = int(rows[-1]["input_rows"])

                if previous_rows > 0 and input_rows < previous_rows * 0.5:
                    print("ALERT: Row-count anomaly detected. Previous=" + str(previous_rows) + ", Current=" + str(input_rows))

        # Data quality
        is_valid, errors = validate_data(df)

        # SLA
        sla_status = calculate_sla_status(df, is_valid)
        save_sla_status(sla_status)

        print(f"SLA Status: {sla_status['overall_status']}")

        # Publish current SLA status
        os.makedirs("data/monitoring", exist_ok=True)

        with open(
            "data/monitoring/current_sla_status.txt",
            "w"
        ) as status_file:
            status_file.write(
                f"Overall SLA: {sla_status['overall_status']}\n"
                f"Freshness: {sla_status['freshness_status']}\n"
                f"Completeness: {sla_status['completeness_status']}\n"
                f"Quality: {sla_status['quality_status']}\n"
            )

        if not is_valid:
            print("DATA QUALITY CHECK FAILED")

            for error in errors:
                print(f"- {error}")

            if sla_status["overall_status"] == "FAIL":
                print("ALERT: Data SLA breach detected.")
                print("ALERT: Owner/consumers should be notified.")

            raise ValueError(
                "Pipeline stopped because data quality checks failed."
            )

        print("DATA QUALITY CHECK PASSED")

        # Transform
        transformed_df = transform_data(df)
        output_rows = len(transformed_df)

        print(f"Output rows: {output_rows}")

        # Publish only after successful validation
        transformed_df.to_csv(
            OUTPUT_FILE,
            index=False
        )

        end_time = datetime.now()

        record_run(
            status="SUCCESS",
            start_time=start_time,
            end_time=end_time,
            input_rows=input_rows,
            output_rows=output_rows,
            quality_status=sla_status["quality_status"],
            freshness_status=sla_status["freshness_status"],
            sla_status=sla_status["overall_status"]
        )

        print("Pipeline completed successfully.")

    except Exception as error:
        end_time = datetime.now()

        record_run(
            status="FAILED",
            start_time=start_time,
            end_time=end_time,
            input_rows=input_rows,
            output_rows=output_rows,
            quality_status="FAIL",
            freshness_status="FAIL",
            sla_status="FAIL",
            failed_stage="Data Quality / SLA",
            error_message=str(error),
        downstream_impact="Output dataset not published; downstream consumers protected",
        )

        raise


if __name__ == "__main__":
    run_pipeline()
