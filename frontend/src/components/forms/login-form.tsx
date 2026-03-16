import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

interface LoginFormProps {
  onLogin: () => void;
}

export default function LoginForm({ onLogin }: LoginFormProps) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (email && password) {
      onLogin();
    } else {
      alert('Please fill in all fields');
    }
  };

  const handleCreateAccount = () => {
    navigate('/create-account');
  };

  return (
    <div style={{
      padding: '40px',
      maxWidth: '420px',
      margin: '80px auto',
      backgroundColor: 'var(--color-surface)',
      borderRadius: '8px',
      border: '1px solid var(--color-border)',
      boxShadow: '0 4px 16px rgba(30,50,112,0.12)',
    }}>
      <h1 style={{ color: 'var(--font-dark)', marginTop: 0 }}>Login</h1>
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '15px' }}>
          <label style={{ color: 'var(--font-dark)', fontWeight: 600 }}>
            Email:
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              style={{ display: 'block', marginTop: '5px', padding: '8px', width: '100%', boxSizing: 'border-box', border: '1px solid var(--color-border)', borderRadius: '4px' }}
            />
          </label>
        </div>

        <div style={{ marginBottom: '15px' }}>
          <label style={{ color: 'var(--font-dark)', fontWeight: 600 }}>
            Password:
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              style={{ display: 'block', marginTop: '5px', padding: '8px', width: '100%', boxSizing: 'border-box', border: '1px solid var(--color-border)', borderRadius: '4px' }}
            />
          </label>
        </div>

        <button
          type="submit"
          style={{
            padding: '10px 20px',
            backgroundColor: 'transparent',
            color: 'var(--color-secondary)',
            border: '2px solid var(--color-secondary)',
            cursor: 'pointer',
            width: '100%',
            marginBottom: '10px',
            borderRadius: '20px',
            fontWeight: 700,
            fontSize: '1rem',
            outline: 'none',
            transition: 'background-color 0.2s, color 0.2s',
          }}
          onMouseEnter={e => { (e.currentTarget as HTMLButtonElement).style.backgroundColor = 'var(--color-secondary)'; (e.currentTarget as HTMLButtonElement).style.color = 'var(--font-light)'; }}
          onMouseLeave={e => { (e.currentTarget as HTMLButtonElement).style.backgroundColor = 'transparent'; (e.currentTarget as HTMLButtonElement).style.color = 'var(--color-secondary)'; }}
        >
          Login
        </button>
      </form>

      <button
        onClick={handleCreateAccount}
        style={{
          padding: '10px 20px',
          backgroundColor: 'transparent',
          color: 'var(--color-accent)',
          border: '2px solid var(--color-accent)',
          cursor: 'pointer',
          width: '100%',
          borderRadius: '20px',
          fontWeight: 600,
          fontSize: '1rem',
          outline: 'none',
          transition: 'background-color 0.2s, color 0.2s',
        }}
        onMouseEnter={e => { (e.currentTarget as HTMLButtonElement).style.backgroundColor = 'var(--color-accent)'; (e.currentTarget as HTMLButtonElement).style.color = 'var(--font-light)'; }}
        onMouseLeave={e => { (e.currentTarget as HTMLButtonElement).style.backgroundColor = 'transparent'; (e.currentTarget as HTMLButtonElement).style.color = 'var(--color-accent)'; }}
      >
        Create Account
      </button>
    </div>
  );
}