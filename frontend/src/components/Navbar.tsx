import { Link } from 'react-router-dom';

export default function Navbar() {
  return (
    <nav style={{ borderBottom: '1px solid #ccc', padding: '10px' }}>
      <Link to="/" style={{ marginRight: '15px' }}>Home</Link>
      <Link to="/catalog" style={{ marginRight: '15px' }}>Catalog</Link>
      <Link to="/checkout" style={{ marginRight: '15px' }}>Checkout</Link>
      <Link to="/create-account" style={{ marginRight: '15px' }}>Create Account</Link>
      <Link to="/order-history" style={{ marginRight: '15px' }}>Order History</Link>
      <Link to="/login">Login</Link>
    </nav>
  );
}
