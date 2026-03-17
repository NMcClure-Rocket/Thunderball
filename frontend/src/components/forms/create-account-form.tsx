import { useNavigate } from 'react-router-dom';
import { useState } from 'react';

export default function CreateAccountForm() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    password: '',
    confirmPassword: ''
  });

  const handleGoBack = () => {
    navigate('/');
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (formData.password !== formData.confirmPassword) {
      alert('Passwords do not match');
      return;
    }
    if (!formData.firstName || !formData.lastName || !formData.email || !formData.password) {
      alert('Please fill in all fields');
      return;
    }
    alert('Account created successfully!');
    // Here you would normally send data to your backend
    navigate('/'); // Redirect back to login
  };

  return (
    <div className="shipping-form-wrapper">
      <button
        onClick={handleGoBack}
        style={{
          padding: '8px 16px',
          backgroundColor: '#6c757d',
          color: 'white',
          border: 'none',
          cursor: 'pointer',
          borderRadius: '4px',
          marginBottom: '20px'
        }}
      >
        ← Go Back
      </button>

      <h1>Create Account:</h1>
      <div className="form-wrapper">
        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: '15px' }}>
            <label>
              First Name:
              <input
                type="text"
                name="firstName"
                value={formData.firstName}
                onChange={handleChange}
                style={{ display: 'block', marginTop: '5px', padding: '8px', width: '100%', boxSizing: 'border-box' }}
              />
            </label>
          </div>

          <div style={{ marginBottom: '15px' }}>
            <label>
              Last Name:
              <input
                type="text"
                name="lastName"
                value={formData.lastName}
                onChange={handleChange}
                style={{ display: 'block', marginTop: '5px', padding: '8px', width: '100%', boxSizing: 'border-box' }}
              />
            </label>
          </div>

          <div style={{ marginBottom: '15px' }}>
            <label>
              Email:
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                style={{ display: 'block', marginTop: '5px', padding: '8px', width: '100%', boxSizing: 'border-box' }}
              />
            </label>
          </div>

          <div style={{ marginBottom: '15px' }}>
            <label>
              Password:
              <input
                type="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                style={{ display: 'block', marginTop: '5px', padding: '8px', width: '100%', boxSizing: 'border-box' }}
              />
            </label>
          </div>

          <div style={{ marginBottom: '15px' }}>
            <label>
              Confirm Password:
              <input
                type="password"
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleChange}
                style={{ display: 'block', marginTop: '5px', padding: '8px', width: '100%', boxSizing: 'border-box' }}
              />
            </label>
          </div>

          <button
            type="submit"
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
        </form>
      </div>
    </div>
  );
}