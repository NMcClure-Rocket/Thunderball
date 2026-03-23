import { useEffect, useRef, useState } from 'react';
import LoginForm from '../components/forms/login-form';
import loginBG from '../assets/LoginBG.png';
import '../css/login-page.css';

interface LoginPageProps {
  onLogin: () => void;
}

export default function LoginPage({ onLogin }: LoginPageProps) {
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const [isMusicOn, setIsMusicOn] = useState(false);
  const [audioReady, setAudioReady] = useState(false);

  useEffect(() => {
    document.body.classList.add('login-page');
    document.body.style.setProperty('--login-bg-image', `url('${loginBG}')`);
    
    return () => {
      if (audioRef.current) {
        audioRef.current.pause();
        audioRef.current.currentTime = 0;
      }
      audioRef.current = null;
      document.body.classList.remove('login-page');
      document.body.style.removeProperty('--login-bg-image');
    };
  }, []);

  const handleToggleMusic = async () => {
    const audio = audioRef.current;
    if (!audio) {
      return;
    }

    if (!audio.paused) {
      audio.pause();
      setIsMusicOn(false);
      return;
    }

    try {
      audio.muted = false;
      await audio.play();
      setIsMusicOn(true);
    } catch {
      setIsMusicOn(false);
    }
  };

  return (
    <>
      <LoginForm onLogin={onLogin} />
      <audio
        ref={audioRef}
        src="/audio/login-music.mp3"
        preload="auto"
        loop
        playsInline
        onCanPlay={() => setAudioReady(true)}
        onPause={() => setIsMusicOn(false)}
        onPlay={() => setIsMusicOn(true)}
        style={{ display: 'none' }}
      />
      <button
        type="button"
        className="login-sound-toggle"
        onClick={handleToggleMusic}
        aria-pressed={isMusicOn}
        disabled={!audioReady}
        title={isMusicOn ? 'Turn music off' : 'Turn music on'}
      >
        {audioReady ? (isMusicOn ? 'Sound: On' : 'Sound: Off') : 'Sound: Loading'}
      </button>
    </>
  );
}
