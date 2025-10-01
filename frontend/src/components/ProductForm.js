import { useState, useEffect } from "react";

export default function ProductForm({ initial, onSave, onCancel }) {
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [price, setPrice] = useState("");
  const [quantity, setQuantity] = useState("");
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    if (initial) {
      setName(initial.name || "");
      setDescription(initial.description || "");
      setPrice(initial.price ?? "");
      setQuantity(initial.quantity ?? "");
    }
  }, [initial]);

  async function submit(e) {
    e.preventDefault();
    setSaving(true);
    try {
      await onSave({
        name,
        description,
        price: parseFloat(price || 0),
        quantity: parseInt(quantity || 0, 10),
      });
    } finally {
      setSaving(false);
    }
  }

  return (
    <form onSubmit={submit} style={{ display: "grid", gap: 8, maxWidth: 420 }}>
      <input placeholder="Name" value={name} onChange={e => setName(e.target.value)} required />
      <input placeholder="Description" value={description} onChange={e => setDescription(e.target.value)} />
      <input placeholder="Price" type="number" step="0.01" value={price} onChange={e => setPrice(e.target.value)} required />
      <input placeholder="Quantity" type="number" value={quantity} onChange={e => setQuantity(e.target.value)} required />
      <div style={{ display: "flex", gap: 8 }}>
        <button type="submit" disabled={saving}>{initial ? "Update" : "Create"}</button>
        <button type="button" onClick={onCancel} disabled={saving}>Cancel</button>
      </div>
    </form>
  );
}
