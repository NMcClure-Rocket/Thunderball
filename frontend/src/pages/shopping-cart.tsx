import { useState, useEffect } from 'react';
import CCInfoForm from '../components/forms/cc-info-form';
import ShippingAddressForm from '../components/forms/shipping-address-form';
import '../css/forms.css';

interface CartItem {
  itemId: string;
  priceId: string;
  name: string;
  description: string;
  format: string;
  potency: number;
  reusable: boolean;
  category: string;
  price: string;
  imageLink: string;
  quantity: number;
}

export default function ShoppingCart() {
  const [cartItems, setCartItems] = useState<CartItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch cart from local storage
    const cart = JSON.parse(localStorage.getItem('cart') || '[]');
    console.log('Cart items:', cart);
    setCartItems(cart);
    setLoading(false);
  }, []);

  if (loading) {
    return <div><h1>Loading...</h1></div>;
  }

  if (cartItems.length === 0) {
    return (
      <div>
        <h1>Shopping Cart</h1>
        <p>Your cart is empty</p>
      </div>
    );
  }

  return (
    <div>

      <div style={{ marginTop: '20px' }}>
      <h3>Total Items: {cartItems.length}</h3>
      <h3>Total Price: ${cartItems.reduce((sum, item) => sum + (parseFloat(item.price) * item.quantity), 0).toFixed(2)}</h3>
    </div>

    <div style={{ marginTop: '20px' }}>
      <h3>Raw JSON Data:</h3>
      <pre>
        {JSON.stringify(cartItems, null, 2)}
      </pre>
    </div>

    {/* <div className="shipping-address-form-div">
      <ShippingAddressForm />
    </div> */}

    <div className="cc-info-form-div">
      <CCInfoForm />
    </div>
    </div>
  );
}