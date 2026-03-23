import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import featSpellsImage from '../assets/Feat-spells.png';
import homeBGImage from '../assets/HomeBG.png';
import bookSymImage from '../assets/BookSym.png';
import cartSymImage from '../assets/CartSym.png';
import histSymImage from '../assets/HistSym.png';
import docSymImage from '../assets/DocSym.png';
import aboutSymImage from '../assets/AboutSym.png';
import '../css/home.css';

export const HomePage: React.FC = () => {
  const navigate = useNavigate();
  const baseURL = "http://localhost:8000";
  const featuredSpells = [
    { name: 'Null Pointer Curse', price: '89.99', img: '/assets/base/null-pointer-curse.png' },
    { name: 'Merge Conflict Doom', price: '139.99', img: '/assets/base/merge-conflict-doom.png' },
    { name: 'Cloud Summon', price: '224.50', img: '/assets/base/cloud-summon.png' },
    { name: 'Deploy Surge', price: '199.99', img: '/assets/base/deploy-surge.png' },
  ];

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
      <button
        className="home-page-about-symbol"
        onClick={() => navigate('/about')}
        aria-label="Go to About Us"
      >
        <img src={aboutSymImage} alt="About symbol" className="home-page-about-symbol-img" />
      </button>
      <button
        className="home-page-book-symbol"
        onClick={() => navigate('/catalog')}
        aria-label="Go to catalog"
      >
        <img src={bookSymImage} alt="Book symbol" className="home-page-book-symbol-img" />
      </button>
      <button
        className="home-page-hist-symbol"
        onClick={() => navigate('/order-history')}
        aria-label="Go to order history"
      >
        <img src={histSymImage} alt="History symbol" className="home-page-hist-symbol-img" />
      </button>
      <button
        className="home-page-cart-symbol"
        onClick={() => navigate('/shopping-cart')}
        aria-label="Go to shopping cart"
      >
        <img src={cartSymImage} alt="Cart symbol" className="home-page-cart-symbol-img" />
      </button>
      <button
        className="home-page-doc-symbol"
        onClick={() => window.location.href = 'http://127.0.0.1:8001/Release-Notes/Release-Notes-v-0.0.1/'}
        aria-label="Go to API documentation"
      >
        <img src={docSymImage} alt="Documentation symbol" className="home-page-doc-symbol-img" />
      </button>
      <div className="home-page-right-column">
        <img className="home-page-feature-image" src={featSpellsImage} alt="Featured spells" />
        <div className="home-page-featured-row home-page-featured-row-top">
          {featuredSpells.slice(0, 2).map((spell) => (
            <div key={spell.name} className="home-page-spell-card">
              <img src={`${baseURL}${spell.img}`} alt={spell.name} className="home-page-spell-img" />
              <h3>{spell.name}</h3>
              <p>${spell.price}</p>
            </div>
          ))}
        </div>
        <div className="home-page-featured-row">
          {featuredSpells.slice(2, 4).map((spell) => (
            <div key={spell.name} className="home-page-spell-card">
              <img src={`${baseURL}${spell.img}`} alt={spell.name} className="home-page-spell-img" />
              <h3>{spell.name}</h3>
              <p>${spell.price}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
