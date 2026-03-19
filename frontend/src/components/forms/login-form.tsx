import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import loginPanel from '../../assets/LoginPanel.png';

interface LoginFormProps {
  onLogin: () => void;
}

export default function LoginForm({ onLogin }: LoginFormProps) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [isLoginHovered, setIsLoginHovered] = useState(false);
  const [isCreateHovered, setIsCreateHovered] = useState(false);
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
          email: email,
          pass: password
        })
      });
        console.log(response)
      // Check if response is successful
      if (response.status === 200) {
        const data = await response.json();
        console.log('Login successful:', data);
        // Save customerid to localStorage
      if (data.customerid) {
        localStorage.setItem('customerid', data.customerid.toString());
        console.log("Saved customerid:", data.customerid);
      }
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
      position: 'relative',
      width: 'min(96vw, 1000px)',
      maxWidth: '1000px',
      minHeight: '560px',
      aspectRatio: '3 / 2',
      margin: '0 auto',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      overflow: 'hidden',
    }}>
      <img
        src={loginPanel}
        alt=""
        aria-hidden="true"
        style={{
          position: 'absolute',
          inset: 0,
          width: '100%',
          height: '100%',
          objectFit: 'contain',
          pointerEvents: 'none',
          userSelect: 'none'
        }}
      />

      <div style={{
        position: 'relative',
        zIndex: 1,
        width: 'min(88%, 900px)',
        padding: '28px 36px'
      }}>
      <h1 style={{ color: '#ffe769', fontSize: '40px', letterSpacing: '0.6px', marginTop: 0, textShadow: '0 0 8px rgba(255, 234, 120, 0.9), 0 0 18px rgba(255, 215, 0, 0.7)' }}>Login</h1>
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '15px' }}>
          <label style={{ color: '#ffe769', fontWeight: 700, fontSize: '24px', textShadow: '0 0 6px rgba(255, 234, 120, 0.85), 0 0 14px rgba(255, 215, 0, 0.65)' }}>
            Email:
            <input

              value={email}
              onChange={(e) => setEmail(e.target.value)}
              disabled={loading}
              style={{ display: 'block', marginTop: '5px', marginLeft: 'auto', marginRight: 'auto', padding: '8px', width: '72%', maxWidth: '460px', minWidth: '260px', boxSizing: 'border-box' }}
            />
          </label>
        </div>

        <div style={{ marginBottom: '15px' }}>
          <label style={{ color: '#ffe769', fontWeight: 700, fontSize: '24px', textShadow: '0 0 6px rgba(255, 234, 120, 0.85), 0 0 14px rgba(255, 215, 0, 0.65)' }}>
            Password:
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              disabled={loading}
              style={{ display: 'block', marginTop: '5px', marginLeft: 'auto', marginRight: 'auto', padding: '8px', width: '72%', maxWidth: '460px', minWidth: '260px', boxSizing: 'border-box' }}
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
          onMouseEnter={() => setIsLoginHovered(true)}
          onMouseLeave={() => setIsLoginHovered(false)}
          style={{
            padding: '10px 20px',
            backgroundColor: loading ? '#6c757d' : '#6f42c1',
            color: isLoginHovered && !loading ? '#ffd84d' : '#ffffff',
            fontSize: '20px',
            fontWeight: 700,
            textShadow: '0 0 8px rgba(255, 234, 120, 0.75), 0 0 16px rgba(255, 215, 0, 0.55)',
            border: 'none',
            cursor: loading ? 'not-allowed' : 'pointer',
            transform: isLoginHovered && !loading ? 'scale(1.08)' : 'scale(1)',
            transition: 'transform 0.18s ease, color 0.18s ease',
            display: 'block',
            width: '72%',
            maxWidth: '460px',
            minWidth: '260px',
            marginLeft: 'auto',
            marginRight: 'auto',
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
        onMouseEnter={() => setIsCreateHovered(true)}
        onMouseLeave={() => setIsCreateHovered(false)}
        style={{
          padding: '10px 20px',
          backgroundColor: '#1f6feb',
          color: isCreateHovered && !loading ? '#ffd84d' : '#ffffff',
          fontSize: '20px',
          fontWeight: 700,
          textShadow: '0 0 8px rgba(255, 234, 120, 0.75), 0 0 16px rgba(255, 215, 0, 0.55)',
          border: 'none',
          cursor: loading ? 'not-allowed' : 'pointer',
          transform: isCreateHovered && !loading ? 'scale(1.08)' : 'scale(1)',
          transition: 'transform 0.18s ease, color 0.18s ease',
          display: 'block',
          width: '72%',
          maxWidth: '460px',
          minWidth: '260px',
          marginLeft: 'auto',
          marginRight: 'auto',
          borderRadius: '4px',
          opacity: loading ? 0.6 : 1
        }}
      >
        Create Account
      </button>
      </div>
    </div>
  );
}