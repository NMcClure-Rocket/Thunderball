import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

interface LoginFormProps {
  onLogin: () => void;
}

export default function LoginForm({ onLogin }: LoginFormProps) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();
  const baseURL = "http://localhost:8000";
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    // Validation
    if (!email || !password) {
      setError('Please fill in all fields');
      setLoading(false);
      return;
    }

    try {
      // Call the POST /logon endpoint
      const response = await fetch(`${baseURL}/logon`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          user: email,
          pass: password
        })
      });
        console.log(response)
      // Check if response is successful
      if (response.status === 200) {
        const data = await response.json();
        console.log('Login successful:', data);
        localStorage.removeItem('cart');
        onLogin();
      } else if (response.status === 401) {
        const data = await response.json();
        setError(data.status || 'Invalid credentials');
      } else {
        setError('An error occurred. Please try again.');
      }
    } catch (err) {
      console.error('Error during login:', err);
      setError('Failed to connect to server');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateAccount = () => {
    navigate('/create-account');
  };
// type="email" <----- PUT THIS IN THE EMAIL INPUT BOX (LINE 72)
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

              value={email}
              onChange={(e) => setEmail(e.target.value)}
              disabled={loading}
              style={{ display: 'block', marginTop: '5px', padding: '8px', width: '100%', boxSizing: 'border-box' }}
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
              disabled={loading}
              style={{ display: 'block', marginTop: '5px', padding: '8px', width: '100%', boxSizing: 'border-box' }}
            />
          </label>
        </div>

        {error && (
          <div style={{
            marginBottom: '15px',
            padding: '10px',
            backgroundColor: '#f8d7da',
            color: '#721c24',
            borderRadius: '4px',
            border: '1px solid #f5c6cb'
          }}>
            {error}
          </div>
        )}

        <button
          type="submit"
          disabled={loading}
          style={{
            padding: '10px 20px',
            backgroundColor: loading ? '#6c757d' : '#007bff',
            color: 'white',
            border: 'none',
            cursor: loading ? 'not-allowed' : 'pointer',
            width: '100%',
            marginBottom: '10px',
            borderRadius: '4px',
            opacity: loading ? 0.6 : 1
          }}
        >
          {loading ? 'Logging in...' : 'Submit'}
        </button>
      </form>

      <button
        onClick={handleCreateAccount}
        disabled={loading}
        style={{
          padding: '10px 20px',
          backgroundColor: '#28a745',
          color: 'white',
          border: 'none',
          cursor: loading ? 'not-allowed' : 'pointer',
          width: '100%',
          borderRadius: '4px',
          opacity: loading ? 0.6 : 1
        }}
      >
        Create Account
      </button>
    </div>
  );
}