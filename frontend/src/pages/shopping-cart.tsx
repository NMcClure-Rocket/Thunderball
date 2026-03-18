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
  const [showShippingForm, setShowShippingForm] = useState(false);
  const [showCCForm, setShowCCForm] = useState(false);

  useEffect(() => {
    // Fetch cart from local storage
    const cart = JSON.parse(localStorage.getItem('cart') || '[]');
    console.log('Cart items:', cart);
    setCartItems(cart);
    setLoading(false);
  }, []);

  const handleRemoveItem = (index: number) => {
    const updatedCart = cartItems.filter((_, i) => i !== index);
    setCartItems(updatedCart);
    localStorage.setItem('cart', JSON.stringify(updatedCart));
  };

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

  const total = cartItems.reduce((sum, item) => sum + (parseFloat(item.price) * item.quantity), 0);

  return (
    <div>
      <h1>Shopping Cart</h1>

      <div style={{ marginTop: '20px', marginBottom: '20px' }}>
        <h3>Items in Cart:</h3>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          {cartItems.map((item, index) => (
            <div key={index} style={{ border: '1px solid #ddd', padding: '15px', borderRadius: '8px', display: 'flex', gap: '15px', alignItems: 'flex-start' }}>
              <img src={item.imageLink} alt={item.name} style={{ width: '100px', height: '100px', objectFit: 'cover', borderRadius: '4px' }} />
              
              <div style={{ flex: 1 }}>
                <h3>{item.name}</h3>
                <p>{item.description}</p>
                <p><strong>Format:</strong> {item.format}</p>
                <p><strong>Potency:</strong> {item.potency}</p>
                <p><strong>Reusable:</strong> {item.reusable ? 'Yes' : 'No'}</p>
                <p><strong>Price per unit:</strong> ${parseFloat(item.price).toFixed(2)}</p>
                <p><strong>Quantity:</strong> {item.quantity}</p>
                <p><strong>Subtotal:</strong> ${(parseFloat(item.price) * item.quantity).toFixed(2)}</p>
              </div>

              <button onClick={() => handleRemoveItem(index)} style={{ padding: '8px 12px', backgroundColor: '#ff4444', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
                🗑️ Remove
              </button>
            </div>
          ))}
        </div>
      </div>

      <div style={{ marginTop: '20px', marginBottom: '20px', padding: '15px', backgroundColor: '#f9f9f9', borderRadius: '8px' }}>
        <h3>Total Items: {cartItems.length}</h3>
        <h3>Total Price: ${total.toFixed(2)}</h3>
        <button type="submit">Submit order</button>
      </div>

      <div className="shipping-address-form-div">
        <button onClick={() => setShowShippingForm(!showShippingForm)}>
          {showShippingForm ? 'Hide Shipping Form' : 'Show Shipping Form'}
        </button>
        {showShippingForm && <ShippingAddressForm />}
      </div>

      <div className="cc-info-form-div">
        <button onClick={() => setShowCCForm(!showCCForm)}>
          {showCCForm ? 'Hide Payment Form' : 'Show Payment Form'}
        </button>
        {showCCForm && <CCInfoForm />}
      </div>
    </div>
  );
}