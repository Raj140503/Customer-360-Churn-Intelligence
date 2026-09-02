import pandas as pd


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and transform raw transaction data."""

    df = df.copy()

    # 1. Standardize column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # 2. Convert CustomerID to nullable integer
    df["customerid"] = df["customerid"].astype("Int64")

    # 3. Remove exact duplicate transactions
    df = df.drop_duplicates()

    # 4. Calculate transaction revenue
    df["revenue"] = df["quantity"] * df["unitprice"]

    # 5. Classify transaction type
    df["transaction_type"] = "SALE"

    df.loc[
        df["invoiceno"].astype(str).str.startswith("C"),
        "transaction_type"
    ] = "RETURN"

    # 6. Create valid sales flag
    df["is_valid_sale"] = (
        (df["transaction_type"] == "SALE")
        & (df["quantity"] > 0)
        & (df["unitprice"] > 0)
        & (df["customerid"].notna())
    )

    return df