from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from datetime import datetime
import pandas as pd
import os

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))


def build_features() -> pd.DataFrame:
    with engine.connect() as conn:
        products = pd.read_sql(text("SELECT * FROM products"), conn)
        sales = pd.read_sql(text("SELECT * FROM sales"), conn)

    now = datetime.utcnow()
    rows = []

    for _, product in products.iterrows():
        product_sales = sales[sales["product_id"] == product["id"]]

        if len(product_sales) == 0:
            # No sales at all — treat as never sold
            days_since_last_sale = 9999
            total_sold_30d = 0
            total_sold_90d = 0
        else:
            last_sale_date = product_sales["created_at"].max()
            days_since_last_sale = (now - last_sale_date).days

            sold_30d = product_sales[
                product_sales["created_at"] >= now - pd.Timedelta(days=30)
            ]
            sold_90d = product_sales[
                product_sales["created_at"] >= now - pd.Timedelta(days=90)
            ]

            total_sold_30d = sold_30d["qty_sold"].sum()
            total_sold_90d = sold_90d["qty_sold"].sum()

        stock_qty = product["stock_qty"]
        cost_per_unit = float(product["cost_per_unit"])
        capital_tied = stock_qty * cost_per_unit

        turnover_rate = (total_sold_90d / stock_qty) if stock_qty > 0 else 0

        rows.append({
            "product_id": product["id"],
            "name": product["name"],
            "days_since_last_sale": days_since_last_sale,
            "total_sold_30d": total_sold_30d,
            "total_sold_90d": total_sold_90d,
            "capital_tied": capital_tied,
            "turnover_rate": turnover_rate,
        })

    return pd.DataFrame(rows)


if __name__ == "__main__":
    df = build_features()
    print(df)