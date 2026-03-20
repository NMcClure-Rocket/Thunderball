import { Routes, Route, useLocation } from 'react-router-dom';
import Navbar from './Navbar';
import { HomePage } from '../pages/home-page';
import Main from '../pages/main';
import Catalog from '../pages/catalog';
import Checkout from '../pages/checkout';
//import CreateAccount from '../pages/create-acc';
import OrderHistory from '../pages/order-hist';
import ShoppingCart from '../pages/shopping-cart';
import About from '../pages/about';

export default function MainApp({ onLogout }: { onLogout: () => void }) {
  const location = useLocation();
  const isCatalogPage = location.pathname === '/catalog';
  const isHomePage = location.pathname === '/';
  const isOrderHistoryPage = location.pathname === '/order-history';
  const isAboutPage = location.pathname === '/about';

  return (
    <div style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh', backgroundColor: (isCatalogPage || isHomePage || isOrderHistoryPage || isAboutPage) ? 'transparent' : 'var(--color-bg)' }}>
      <Navbar onLogout={onLogout} />
      <div style={{ paddingTop: '28px' }}>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/catalog" element={<Catalog />} />
          <Route path="/checkout" element={<Checkout />} />
          <Route path="/shopping-cart" element={<ShoppingCart />} />
          <Route path="/order-history" element={<OrderHistory />} />
          <Route path="/about" element={<About />} />
        </Routes>
      </div>
    </div>
  );
}
