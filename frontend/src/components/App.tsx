import { useState } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import '../css/App.css';
import LoginPage from '../pages/login-page';
import MainApp from './MainApp';

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
        {/* If not logged in, show login page */}
        {!isLoggedIn ? (
          <Route path="*" element={<LoginPage onLogin={handleLogin} />} />
        ) : (
          /* If logged in, show the main app with navbar and routes */
          <Route path="*" element={<MainApp onLogout={handleLogout} />} />
        )}
      </Routes>
    </BrowserRouter>
  );
}

export default App;
