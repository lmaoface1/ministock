from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))

with engine.connect() as conn:
    # Clear old data first
    conn.execute(text("DELETE FROM sales"))
    conn.execute(text("DELETE FROM products"))
    conn.commit()

    products = [
        # name, category, stock_qty, cost_per_unit
        ("Cement Bag", "Construction", 50, 250.00),
        ("Steel Nail 1kg", "Hardware", 200, 80.00),
        ("PVC Pipe 4in", "Plumbing", 5, 320.00),     # will be frozen
        ("Paint Bucket White", "Paint", 10, 450.00), # will be frozen
        ("Hammer", "Tools", 30, 180.00),
        ("Plywood Sheet", "Construction", 2, 600.00), # will be frozen
        ("Electrical Wire 10m", "Electrical", 40, 150.00),
        ("Sandpaper Pack", "Tools", 100, 35.00),
    ]

    product_ids = {}
    for name, category, stock_qty, cost in products:
        result = conn.execute(
            text("""
                INSERT INTO products (name, category, stock_qty, cost_per_unit)
                VALUES (:name, :category, :stock_qty, :cost)
                RETURNING id
            """),
            {"name": name, "category": category, "stock_qty": stock_qty, "cost": cost}
        )
        product_ids[name] = result.fetchone()[0]
        conn.commit()

    # Recent sales (within last 30 days) — these products are NOT frozen
    recent_sales = [
        ("Cement Bag", 5, 10),
        ("Steel Nail 1kg", 20, 5),
        ("Hammer", 3, 15),
        ("Electrical Wire 10m", 10, 20),
        ("Sandpaper Pack", 15, 2),
    ]

    for name, qty, days_ago in recent_sales:
        conn.execute(
            text("""
                INSERT INTO sales (product_id, qty_sold, created_at)
                VALUES (:pid, :qty, :date)
            """),
            {
                "pid": product_ids[name],
                "qty": qty,
                "date": datetime.utcnow() - timedelta(days=days_ago)
            }
        )
    conn.commit()

    # Old sales (120+ days ago) — these products WILL be frozen (no recent sales)
    old_sales = [
        ("PVC Pipe 4in", 2, 150),
        ("Paint Bucket White", 1, 200),
        ("Plywood Sheet", 1, 180),
    ]

    for name, qty, days_ago in old_sales:
        conn.execute(
            text("""
                INSERT INTO sales (product_id, qty_sold, created_at)
                VALUES (:pid, :qty, :date)
            """),
            {
                "pid": product_ids[name],
                "qty": qty,
                "date": datetime.utcnow() - timedelta(days=days_ago)
            }
        )
    conn.commit()

print("Seed data inserted successfully.")
