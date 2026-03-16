import { useState } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import LoginPage from '../pages/login-page';
import CreateAccount from '../pages/create-acc';
import MainApp from './MainApp';
import '../css/App.css'; // ← Add this import

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const handleLogin = () => {
    setIsLoggedIn(true);
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
  };

  return (
    <BrowserRouter>
      <Routes>
        {!isLoggedIn ? (
          <>
            <Route path="/" element={<LoginPage onLogin={handleLogin} />} />
            <Route path="/create-account" element={<CreateAccount />} />
            <Route path="*" element={<LoginPage onLogin={handleLogin} />} />
          </>
        ) : (
          <Route path="*" element={<MainApp onLogout={handleLogout} />} />
        )}
      </Routes>
    </BrowserRouter>
  );
}

export default App;
