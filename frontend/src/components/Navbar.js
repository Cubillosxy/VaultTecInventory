import { useNavigate, Link } from "react-router-dom";
import { logout } from "../api";

export default function Navbar() {
  const navigate = useNavigate();
  const token = !!localStorage.getItem("token");

  function onLogout() {
    logout();
    navigate("/login");
  }

  return (
    <div style={{ display: "flex", gap: 12, padding: 12, borderBottom: "1px solid #e5e5e5" }}>
      <Link to="/">Inventory</Link>
      <div style={{ marginLeft: "auto" }}>
        {token ? <button onClick={onLogout}>Logout</button> : <Link to="/login">Login</Link>}
      </div>
    </div>
  );
}
