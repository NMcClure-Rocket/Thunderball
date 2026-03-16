import { Routes, Route } from 'react-router-dom';
import Navbar from './Navbar';
import Footer from './Footer';
import Main from '../pages/main';
import Catalog from '../pages/catalog';
import Checkout from '../pages/checkout';
//import CreateAccount from '../pages/create-acc';
import OrderHistory from '../pages/order-hist';

export default function MainApp({ onLogout }: { onLogout: () => void }) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <Navbar onLogout={onLogout} />
      <div style={{ flex: 1 }}>
        <Routes>
          <Route path="/" element={<Main />} />
          <Route path="/catalog" element={<Catalog />} />
          <Route path="/checkout" element={<Checkout />} />
          <Route path="/order-history" element={<OrderHistory />} />
        </Routes>
      </div>
      <Footer />
    </div>
  );
}
