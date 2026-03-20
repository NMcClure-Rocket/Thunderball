import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import cartIcon from '../assets/cart.png';

interface NavbarProps {
  onLogout: () => void;
}

function NavLink({ to, children }: { to: string; children: React.ReactNode }) {
  const [hovered, setHovered] = useState(false);
  return (
    <Link
      to={to}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      style={{
        marginRight: '10px',
        padding: '11px 20px',
        fontWeight: 600,
        fontSize: '1.02rem',
        textDecoration: 'none',
        borderRadius: '8px',
        border: '1px solid var(--font-light)',
        display: 'inline-block',
        transition: 'background-color 0.2s, color 0.2s',
        backgroundColor: hovered ? 'var(--font-light)' : 'transparent',
        color: hovered ? 'var(--color-primary)' : 'var(--font-light)',
      }}
    >
      {children}
    </Link>
  );
}

function NavIconLink({ to, children }: { to: string; children: React.ReactNode }) {
  return (
    <Link
      to={to}
      style={{
        marginLeft: '12px',
        padding: '4px 8px',
        display: 'inline-flex',
        alignItems: 'center',
        border: '1px solid var(--font-light)',
        borderRadius: '8px',
        background: 'transparent',
        outline: 'none',
        lineHeight: 0,
        cursor: 'pointer',
      }}
    >
      {children}
    </Link>
  );
}

function NavButton({ onClick, children, gold }: { onClick: () => void; children: React.ReactNode; gold?: boolean }) {
  const [hovered, setHovered] = useState(false);
  const base = gold ? 'var(--color-highlight)' : 'var(--font-light)';
  const dark = gold ? 'var(--color-primary)' : 'var(--color-primary)';
  return (
    <button
      onClick={onClick}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      style={{
        marginLeft: '12px',
        padding: '11px 22px',
        backgroundColor: hovered ? base : 'transparent',
        color: hovered ? dark : base,
        border: `2px solid ${base}`,
        cursor: 'pointer',
        borderRadius: '26px',
        fontWeight: 600,
        fontSize: '1.02rem',
        transition: 'background-color 0.2s, color 0.2s',
        outline: 'none',
      }}
    >
      {children}
    </button>
  );
}

export default function Navbar({ onLogout }: NavbarProps) {
  const navigate = useNavigate();
  const handleLogout = () => {
    // Clear all localStorage
    localStorage.clear();
    console.log("Local storage cleared");
    console.log(localStorage)
    
    // Call the onLogout callback
    onLogout();
    navigate('/');
  };

  return (
    <nav style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      zIndex: 1000,
      backgroundColor: 'var(--color-primary)',
      borderBottom: '3px solid var(--color-secondary)',
      minHeight: '88px',
      padding: '16px 28px',
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
    }}>
      <div style={{ display: 'flex', alignItems: 'center' }}>
        <NavLink to="/">Home</NavLink>
        <NavLink to="/catalog">Catalog</NavLink>
        <NavLink to="/order-history">Order History</NavLink>
      </div>
      <div style={{ display: 'flex', alignItems: 'center' }}>
        <NavIconLink to="/shopping-cart">
          <img src={cartIcon} alt="Shopping Cart" style={{ height: '58px', width: '58px', objectFit: 'contain', display: 'block' }} />
        </NavIconLink>
        <NavButton onClick={handleLogout} gold>Logout</NavButton>
      </div>
    </nav>
  );
}
