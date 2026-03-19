import { useEffect, useRef, useState } from 'react';
import { BrowserRouter, Routes, Route, useLocation } from 'react-router-dom';
import LoginPage from '../pages/login-page';
import CreateAccount from '../pages/create-acc';
import MainApp from './MainApp';
import '../css/App.css';
import Catalog from '../pages/catalog';

interface AppRoutesProps {
  isLoggedIn: boolean;
  onLogin: () => void;
  onLogout: () => void;
}

function AppRoutes({ isLoggedIn, onLogin, onLogout }: AppRoutesProps) {
  const location = useLocation();
  const siteAudioRef = useRef<HTMLAudioElement | null>(null);
  const [isSiteMusicOn, setIsSiteMusicOn] = useState(false);
  const [isSiteAudioReady, setIsSiteAudioReady] = useState(false);

  const isNonLoginPublicPage = location.pathname === '/catalog' || location.pathname === '/create-account';
  const shouldPlaySiteMusic = isLoggedIn || isNonLoginPublicPage;

  useEffect(() => {
    if (!shouldPlaySiteMusic && siteAudioRef.current) {
      siteAudioRef.current.pause();
      siteAudioRef.current.currentTime = 0;
      setIsSiteMusicOn(false);
    }
  }, [shouldPlaySiteMusic]);

  const handleToggleSiteMusic = async () => {
    const audio = siteAudioRef.current;
    if (!audio) {
      return;
    }

    if (!audio.paused) {
      audio.pause();
      setIsSiteMusicOn(false);
      return;
    }

    try {
      audio.muted = false;
      await audio.play();
      setIsSiteMusicOn(true);
    } catch {
      setIsSiteMusicOn(false);
    }
  };

  return (
    <>
      <Routes>
        {!isLoggedIn ? (
          <>
            <Route path="*" element={<LoginPage onLogin={onLogin} />} />
            <Route path="/catalog" element={<Catalog />} />
            <Route path="/create-account" element={<CreateAccount />} />
          </>
        ) : (
          <Route path="*" element={<MainApp onLogout={onLogout} />} />
        )}
      </Routes>

      {shouldPlaySiteMusic && (
        <>
          <audio
            ref={siteAudioRef}
            src="/audio/site-music.mp3"
            preload="auto"
            loop
            playsInline
            onCanPlay={() => setIsSiteAudioReady(true)}
            onPause={() => setIsSiteMusicOn(false)}
            onPlay={() => setIsSiteMusicOn(true)}
            style={{ display: 'none' }}
          />
          <button
            type="button"
            className="site-sound-toggle"
            onClick={handleToggleSiteMusic}
            aria-pressed={isSiteMusicOn}
            disabled={!isSiteAudioReady}
            title={isSiteMusicOn ? 'Turn site music off' : 'Turn site music on'}
          >
            {isSiteAudioReady ? (isSiteMusicOn ? 'Site Sound: On' : 'Site Sound: Off') : 'Site Sound: Loading'}
          </button>
        </>
      )}
    </>
  );
}

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
      <AppRoutes isLoggedIn={isLoggedIn} onLogin={handleLogin} onLogout={handleLogout} />
    </BrowserRouter>
  );
}


export default App;
