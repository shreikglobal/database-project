from extract import extract_data
from transform import transform_data


INPUT_FILE = "data/input/orders.csv"
OUTPUT_FILE = "data/output/processed_orders.csv"


def run_pipeline():
    print("Starting pipeline...")

    df = extract_data(INPUT_FILE)
    print(f"Input rows: {len(df)}")

    transformed_df = transform_data(df)
    print(f"Output rows: {len(transformed_df)}")

    transformed_df.to_csv(OUTPUT_FILE, index=False)

    print("Pipeline completed successfully.")


if __name__ == "__main__":
    run_pipeline()
