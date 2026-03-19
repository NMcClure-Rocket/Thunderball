import { useEffect } from 'react';
import homeBGImage from '../assets/HomeBG.png';
import '../css/home.css';

export default function Main() {
  useEffect(() => {
    document.body.classList.add('home-page');
    document.body.style.setProperty('--home-bg-image', `url('${homeBGImage}')`);
    return () => {
      document.body.classList.remove('home-page');
      document.body.style.removeProperty('--home-bg-image');
    };
  }, []);

  return (
    <div style={{ paddingTop: '80px' }}>
      <h1>Home - Main Page</h1>
      <p>Welcome to Thunderball</p>
    </div>
  );
}
