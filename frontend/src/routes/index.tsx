import { Routes, Route } from 'react-router-dom';
import Main from '../pages/main';
import Catalog from '../pages/catalog';
import Checkout from '../pages/checkout';
import CreateAccount from '../pages/create-acc';
import OrderHistory from '../pages/order-hist';
import ShoppingCart from '../pages/shopping-cart';
import About from '../pages/about';
//import Login from '../components/Login';

export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Main />} />
      <Route path="/catalog" element={<Catalog />} />
      <Route path="/checkout" element={<Checkout />} />
      <Route path="/create-account" element={<CreateAccount />} />
      <Route path="/order-history" element={<OrderHistory />} />
      <Route path="/shopping-cart" element={<ShoppingCart />} />
      <Route path="/about" element={<About />} />
    </Routes>
  );
}
