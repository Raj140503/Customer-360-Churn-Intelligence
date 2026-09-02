from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "Online Retail.xlsx"


def extract_data() -> pd.DataFrame:
    """Read the raw Online Retail dataset."""
    
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_PATH}")

    df = pd.read_excel(DATA_PATH)

    print(f"Successfully extracted {len(df):,} rows.")

    return df


if __name__ == "__main__":
    df = extract_data()

    print(f"Shape: {df.shape}")