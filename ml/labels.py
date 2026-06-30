import pandas as pd


def add_labels(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["is_frozen"] = (
        (df["days_since_last_sale"] > 90) & (df["total_sold_90d"] == 0)
    ).astype(int)
    return df


if __name__ == "__main__":
    from features import build_features

    df = build_features()
    df = add_labels(df)
    print(df[["name", "days_since_last_sale", "total_sold_90d", "is_frozen"]])