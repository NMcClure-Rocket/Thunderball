import { useState, useEffect } from 'react';

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
        <h3>Raw JSON Data:</h3>
        <pre style={{ backgroundColor: '#f0f0f0', padding: '10px', overflow: 'auto' }}>
          {JSON.stringify(cartItems, null, 2)}
        </pre>
      </div>
    </div>
  );
}