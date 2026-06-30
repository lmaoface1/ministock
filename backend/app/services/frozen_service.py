import joblib
import os
from datetime import datetime
from sqlalchemy.orm import Session
from app.models import Product, Sale, FrozenResult

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "ml_artifacts", "frozen_classifier.pkl")
model = joblib.load(MODEL_PATH)

FEATURE_COLUMNS = [
    "days_since_last_sale",
    "total_sold_30d",
    "total_sold_90d",
    "capital_tied",
    "turnover_rate",
]


def compute_features_for_product(db: Session, product: Product, now: datetime):
    sales = db.query(Sale).filter(Sale.product_id == product.id).all()

    if not sales:
        days_since_last_sale = 9999
        total_sold_30d = 0
        total_sold_90d = 0
    else:
        last_sale_date = max(s.created_at for s in sales)
        days_since_last_sale = (now - last_sale_date).days

        total_sold_30d = sum(
            s.qty_sold for s in sales if (now - s.created_at).days <= 30
        )
        total_sold_90d = sum(
            s.qty_sold for s in sales if (now - s.created_at).days <= 90
        )

    stock_qty = product.stock_qty
    cost_per_unit = float(product.cost_per_unit)
    capital_tied = stock_qty * cost_per_unit
    turnover_rate = (total_sold_90d / stock_qty) if stock_qty > 0 else 0

    return {
        "days_since_last_sale": days_since_last_sale,
        "total_sold_30d": total_sold_30d,
        "total_sold_90d": total_sold_90d,
        "capital_tied": capital_tied,
        "turnover_rate": turnover_rate,
    }


def run_frozen_capital_analysis(db: Session):
    products = db.query(Product).all()
    now = datetime.utcnow()

    results = []
    for product in products:
        features = compute_features_for_product(db, product, now)
        X = [[features[col] for col in FEATURE_COLUMNS]]
        is_frozen = int(model.predict(X)[0])

        result = FrozenResult(
            product_id=product.id,
            is_frozen=is_frozen,
            capital_tied=features["capital_tied"],
            generated_at=now,
        )
        db.add(result)
        results.append(result)

    db.commit()
    for r in results:
        db.refresh(r)

    return results


def get_latest_results(db: Session):
    return (
        db.query(FrozenResult)
        .order_by(FrozenResult.generated_at.desc())
        .limit(100)
        .all()
    )