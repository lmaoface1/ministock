import { useState, useEffect } from "react";
import {
  getProducts,
  createSale,
  runFrozenAnalysis,
  getFrozenResults,
} from "./api";

function App() {
  const [products, setProducts] = useState([]);
  const [frozenResults, setFrozenResults] = useState([]);
  const [saleProductId, setSaleProductId] = useState("");
  const [saleQty, setSaleQty] = useState("");
  const [error, setError] = useState("");

  async function loadProducts() {
    const data = await getProducts();
    setProducts(data);
  }

  async function loadFrozenResults() {
    const data = await getFrozenResults();
    setFrozenResults(data);
  }

  useEffect(() => {
    loadProducts();
    loadFrozenResults();
  }, []);

  async function handleSaleSubmit(e) {
    e.preventDefault();
    setError("");
    try {
      await createSale(Number(saleProductId), Number(saleQty));
      setSaleProductId("");
      setSaleQty("");
      await loadProducts();
    } catch (err) {
      setError(err.message);
    }
  }

  async function handleRunAnalysis() {
    await runFrozenAnalysis();
    await loadFrozenResults();
  }

  function isFrozen(productId) {
    const result = frozenResults.find((r) => r.product_id === productId);
    return result ? result.is_frozen === 1 : null;
  }

  return (
    <div className="max-w-3xl mx-auto p-6 space-y-8">
      <h1 className="text-2xl font-bold">MiniStock</h1>

      {/* Products table */}
      <section>
        <h2 className="text-lg font-semibold mb-2">Products</h2>
        <table className="w-full text-sm border">
          <thead>
            <tr className="bg-gray-100 text-left">
              <th className="p-2 border">ID</th>
              <th className="p-2 border">Name</th>
              <th className="p-2 border">Stock</th>
              <th className="p-2 border">Cost/Unit</th>
              <th className="p-2 border">Frozen?</th>
            </tr>
          </thead>
          <tbody>
            {products.map((p) => {
              const frozen = isFrozen(p.id);
              return (
                <tr key={p.id}>
                  <td className="p-2 border">{p.id}</td>
                  <td className="p-2 border">{p.name}</td>
                  <td className="p-2 border">{p.stock_qty}</td>
                  <td className="p-2 border">{p.cost_per_unit}</td>
                  <td className="p-2 border">
                    {frozen === null ? (
                      "—"
                    ) : frozen ? (
                      <span className="text-red-600 font-medium">Frozen</span>
                    ) : (
                      <span className="text-green-600">OK</span>
                    )}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </section>

      {/* Sale form */}
      <section>
        <h2 className="text-lg font-semibold mb-2">Record a Sale</h2>
        <form onSubmit={handleSaleSubmit} className="flex gap-2 items-end">
          <div>
            <label className="block text-sm">Product ID</label>
            <input
              type="number"
              value={saleProductId}
              onChange={(e) => setSaleProductId(e.target.value)}
              className="border rounded p-1 w-24"
              required
            />
          </div>
          <div>
            <label className="block text-sm">Qty Sold</label>
            <input
              type="number"
              value={saleQty}
              onChange={(e) => setSaleQty(e.target.value)}
              className="border rounded p-1 w-24"
              required
            />
          </div>
          <button
            type="submit"
            className="bg-blue-600 text-white rounded px-4 py-1"
          >
            Record Sale
          </button>
        </form>
        {error && <p className="text-red-600 text-sm mt-2">{error}</p>}
      </section>

      {/* Frozen analysis */}
      <section>
        <h2 className="text-lg font-semibold mb-2">Frozen Capital Analysis</h2>
        <button
          onClick={handleRunAnalysis}
          className="bg-gray-800 text-white rounded px-4 py-1"
        >
          Run Analysis
        </button>
      </section>
    </div>
  );
}

export default App;