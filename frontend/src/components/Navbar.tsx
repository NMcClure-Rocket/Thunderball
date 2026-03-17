import { Link } from 'react-router-dom';

interface NavbarProps {
  onLogout: () => void;
}

export default function Navbar({ onLogout }: NavbarProps) {
  return (
    <nav style={{ borderBottom: '1px solid #ccc', padding: '10px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
      <div>
        <Link to="/" style={{ marginRight: '15px' }}>Home</Link>
        <Link to="/catalog" style={{ marginRight: '15px' }}>Catalog</Link>
        <Link to="/shopping-cart" style={{ marginRight: '15px' }}>Shopping Cart</Link>
        <Link to="/order-history" style={{ marginRight: '15px' }}>Order History</Link>
      </div>
      <button
        onClick={onLogout}
        style={{
          padding: '8px 15px',
          backgroundColor: '#dc3545',
          color: 'white',
          border: 'none',
          cursor: 'pointer'
        }}
      >
        Logout
      </button>
    </nav>
  );
}
