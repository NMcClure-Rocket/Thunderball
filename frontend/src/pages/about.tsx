import { useEffect } from 'react';
import aboutBGImage from '../assets/AboutBG.png';
import '../css/about.css';

export default function About() {
  useEffect(() => {
    document.body.classList.add('about-page');
    document.body.style.setProperty('--about-bg-image', `url('${aboutBGImage}')`);
    return () => {
      document.body.classList.remove('about-page');
      document.body.style.removeProperty('--about-bg-image');
    };
  }, []);

  return (
    <div className="about-container">
      <header className="about-header">
        <span className="about-kicker">Est. 2026</span>
        <h1>About Thunderball</h1>
        <p>The premier marketplace for tech-powered spells & arcane solutions</p>
      </header>

      <section className="about-section">
        <h2>Our Mission</h2>
        <p>
          Thunderball was founded on the belief that every developer, sysadmin, and
          tech wizard deserves access to powerful spells that solve real-world problems.
          From <strong>Null Pointer Curses</strong> to <strong>Cloud Summons</strong>,
          our catalog is curated for the modern practitioner of the digital arts.
        </p>
      </section>

      <section className="about-section">
        <h2>What We Offer</h2>
        <div className="about-cards">
          <div className="about-card">
            <h3>Spell Catalog</h3>
            <p>Browse hundreds of tech-themed spells sorted by potency, category, and format.</p>
          </div>
          <div className="about-card">
            <h3>Secure Checkout</h3>
            <p>Fast, reliable transactions backed by authentication and order tracking.</p>
          </div>
          <div className="about-card">
            <h3>Order History</h3>
            <p>Review all past purchases with full delivery estimates and item details.</p>
          </div>
        </div>
      </section>

      <section className="about-section">
        <h2>The Team</h2>
        <p>
          Built by a small team of engineers who wanted to combine their love of fantasy
          RPGs with their day-to-day work in software development. Thunderball is a
          passion project turned platform.
        </p>
      </section>
    </div>
  );
}
