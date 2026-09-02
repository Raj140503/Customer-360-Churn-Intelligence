from pathlib import Path

from test_read import extract_data
from transform import transform_data


PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "sales.csv"


def run_pipeline():
    print("Starting ETL pipeline...")

    # Extract
    df = extract_data()

    # Transform
    df = transform_data(df)

    # Filter valid sales
    sales_df = df[df["is_valid_sale"]].copy()

    print(f"Valid sales records: {len(sales_df):,}")

    # Save processed data
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    sales_df.to_csv(OUTPUT_PATH, index=False)

    print(f"Saved processed data to: {OUTPUT_PATH}")
    print("ETL pipeline completed successfully.")

    return sales_df


if __name__ == "__main__":
    run_pipeline()