import { useEffect, useState } from "react";
import { listProducts, createProduct, updateProduct, deleteProduct } from "../api";
import ProductForm from "./ProductForm";

export default function Dashboard() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [q, setQ] = useState("");
  const [editing, setEditing] = useState(null);
  const [creating, setCreating] = useState(false);

  async function load() {
    setLoading(true);
    setError("");
    try {
      const data = await listProducts(q);
      setItems(data);
    } catch (e) {
      setError("Failed to load products");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { load(); }, []);

  async function onCreate(payload) {
    await createProduct(payload);
    setCreating(false);
    await load();
  }

  async function onUpdate(payload) {
    await updateProduct(editing.id, payload);
    setEditing(null);
    await load();
  }

  async function onDelete(id) {
    if (!window.confirm("Delete this product?")) return;
    await deleteProduct(id);
    await load();
  }

  return (
    <div style={{ maxWidth: 960, margin: "24px auto", padding: "0 12px" }}>
      <h2>Inventory Dashboard</h2>

      <div style={{ display: "flex", gap: 8, marginBottom: 12 }}>
        <input placeholder="Search by name…" value={q} onChange={e => setQ(e.target.value)} />
        <button onClick={load}>Search</button>
        <button onClick={() => { setCreating(true); setEditing(null); }}>New Product</button>
      </div>

      {creating && (
        <div style={{ marginBottom: 16 }}>
          <h4>Create Product</h4>
          <ProductForm onSave={onCreate} onCancel={() => setCreating(false)} />
        </div>
      )}

      {editing && (
        <div style={{ marginBottom: 16 }}>
          <h4>Edit Product</h4>
          <ProductForm initial={editing} onSave={onUpdate} onCancel={() => setEditing(null)} />
        </div>
      )}

      {loading ? <div>Loading…</div> : error ? <div style={{ color: "tomato" }}>{error}</div> : (
        <table width="100%" cellPadding="8" style={{ borderCollapse: "collapse" }}>
          <thead>
            <tr style={{ borderBottom: "1px solid #ddd" }}>
              <th align="left">Name</th>
              <th align="left">Description</th>
              <th align="right">Price</th>
              <th align="right">Quantity</th>
              <th align="center">Actions</th>
            </tr>
          </thead>
          <tbody>
            {items.map(p => (
              <tr key={p.id} style={{ borderBottom: "1px solid #f0f0f0" }}>
                <td>{p.name}</td>
                <td>{p.description}</td>
                <td align="right">{p.price}</td>
                <td align="right">{p.quantity}</td>
                <td align="center" style={{ display: "flex", gap: 8, justifyContent: "center" }}>
                  <button onClick={() => { setEditing(p); setCreating(false); }}>Edit</button>
                  <button onClick={() => onDelete(p.id)}>Delete</button>
                </td>
              </tr>
            ))}
            {items.length === 0 && (
              <tr><td colSpan="5" align="center" style={{ padding: 24, color: "#888" }}>No products</td></tr>
            )}
          </tbody>
        </table>
      )}
    </div>
  );
}
