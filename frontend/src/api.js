const BASE_URL = "http://127.0.0.1:8000";

export async function getProducts() {
  const res = await fetch(`${BASE_URL}/products/`);
  return res.json();
}

export async function createSale(productId, qtySold) {
  const res = await fetch(`${BASE_URL}/sales/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ product_id: productId, qty_sold: qtySold }),
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || "Sale failed");
  }
  return res.json();
}

export async function runFrozenAnalysis() {
  const res = await fetch(`${BASE_URL}/analytics/frozen-capital/run`, {
    method: "POST",
  });
  return res.json();
}

export async function getFrozenResults() {
  const res = await fetch(`${BASE_URL}/analytics/frozen-capital/`);
  return res.json();
}