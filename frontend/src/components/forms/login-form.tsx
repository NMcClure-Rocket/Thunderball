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
    <div style={{ padding: '20px', maxWidth: '400px', margin: '50px auto' }}>
      <h1>Login</h1>
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '15px' }}>
          <label>
            Email:
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              style={{ display: 'block', marginTop: '5px', padding: '8px', width: '100%', boxSizing: 'border-box' }}
            />
          </label>
        </div>

        <div style={{ marginBottom: '15px' }}>
          <label>
            Password:
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              style={{ display: 'block', marginTop: '5px', padding: '8px', width: '100%', boxSizing: 'border-box' }}
            />
          </label>
        </div>

        <button
          type="submit"
          style={{
            padding: '10px 20px',
            backgroundColor: '#007bff',
            color: 'white',
            border: 'none',
            cursor: 'pointer',
            width: '100%',
            marginBottom: '10px',
            borderRadius: '4px'
          }}
        >
          Submit
        </button>
      </form>

      <button
        onClick={handleCreateAccount}
        style={{
          padding: '10px 20px',
          backgroundColor: '#28a745',
          color: 'white',
          border: 'none',
          cursor: 'pointer',
          width: '100%',
          borderRadius: '4px'
        }}
      >
        Create Account
      </button>
    </div>
  );
}