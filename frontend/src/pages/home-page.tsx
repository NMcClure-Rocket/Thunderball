import React, { useEffect } from 'react';
import featSpellsImage from '../assets/Feat-spells.png';
import homeBGImage from '../assets/HomeBG.png';
import '../css/home.css';

export const HomePage: React.FC = () => {
  useEffect(() => {
    document.body.classList.add('home-page');
    document.body.style.setProperty('--home-bg-image', `url('${homeBGImage}')`);
    return () => {
      document.body.classList.remove('home-page');
      document.body.style.removeProperty('--home-bg-image');
    };
  }, []);

  return (
    <div className="home-page-shell">
      <img className="home-page-feature-image" src={featSpellsImage} alt="Featured spells" />
    </div>
  );
};
