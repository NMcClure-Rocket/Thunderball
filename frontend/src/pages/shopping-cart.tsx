import { useState, useEffect } from 'react';
import CCInfoForm from '../components/forms/cc-info-form';
import ShippingAddressForm from '../components/forms/shipping-address-form';
import SubmitPurchaseInfoButton from '../components/buttons/submit-purchase-info-button';

import '../css/forms.css';
import shoppingCartTavern from '../assets/Shopping Cart Tavern.png';
import '../css/shopping-cart.css';

interface CartItem {
  itemId: string;
  // priceId: string;
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
  const [showCheckout, setShowCheckout] = useState(false);

  useEffect(() => {
    document.body.classList.add('shopping-cart-page');
    document.body.style.setProperty('--shopping-cart-bg-image', `url(${shoppingCartTavern})`);

    // Fetch cart from local storage
    const cart = JSON.parse(localStorage.getItem('cart') || '[]');
    setTimeout(() => {
      setCartItems(cart);
      setLoading(false);
    }, 0);

    return () => {
      document.body.classList.remove('shopping-cart-page');
      document.body.style.removeProperty('--shopping-cart-bg-image');
    };
  }, []);

  const displayItems = cartItems.length > 0 ? cartItems : [];
  const isPreviewMode = cartItems.length === 0;
  const subtotal = displayItems.reduce((total, item) => {
    const price = Number.parseFloat(item.price) || 0;
    return total + price * item.quantity;
  }, 0);
  const shipping = subtotal > 40 ? 0 : 6.5;
  const tax = subtotal * 0.07;
  const total = subtotal + shipping + tax;

  const handleRemoveItem = (index: number) => {
    const updatedCart = cartItems.filter((_, i) => i !== index);
    setCartItems(updatedCart);
    localStorage.setItem('cart', JSON.stringify(updatedCart));
  };

  if (loading) {
    return (
      <div className="shopping-cart-shell">
        <div className="shopping-cart-panel shopping-cart-loading">
          <h1>Loading cart...</h1>
          <p>Pulling together your current selections.</p>
        </div>
      </div>
    );
  }

  return (
    <main className="shopping-cart-shell">
      <section className="shopping-cart-panel">
        <header className="shopping-cart-header">
          <div>
            <span className="shopping-cart-kicker">Order review</span>
            <h1>Shopping Cart</h1>
            <p>
              Review the items in your cart before entering shipping and payment details.
            </p>
          </div>
        </header>

        <div className="shopping-cart-grid">
          <div className="shopping-cart-items">
            {cartItems.length === 0 ? (
              <div className="shopping-cart-empty-state">
                <h2>Your cart is empty</h2>
                <p>Add items from the catalog to see them here.</p>
              </div>
            ) : (
              cartItems.map((item, index) => (
                <article key={`${item.itemId}`} className="shopping-cart-card">
                  <div className="shopping-cart-card-media">
                    <img
                      src={`http://localhost:8000${item.imageLink}`}
                      alt={item.name}
                      className="shopping-cart-card-image"
                    />
                  </div>
                  <div className="shopping-cart-card-body">
                    <div className="shopping-cart-card-topline">
                      <div>
                        <h2>{item.name}</h2>
                        <p>{item.description}</p>
                      </div>
                      <strong>${(Number.parseFloat(item.price) || 0).toFixed(2)}</strong>
                    </div>

                    <div className="shopping-cart-meta-row">
                      <span>{item.format}</span>
                      <span>Potency {item.potency}</span>
                      <span>{item.reusable ? 'Reusable' : 'Single use'}</span>
                    </div>

                    <div className="shopping-cart-actions-row">
                      <span className="shopping-cart-quantity-label">Quantity: {item.quantity}</span>
                      <button type="button" className="shopping-cart-text-button" onClick={() => handleRemoveItem(index)}>
                        Remove
                      </button>
                    </div>
                  </div>
                </article>
              ))
            )}
          </div>

          <aside className="shopping-cart-summary">
            <div className="shopping-cart-summary-card">
              <h2>Order Summary</h2>
              <div className="shopping-cart-summary-row">
                <span>Items</span>
                <strong>{cartItems.reduce((count, item) => count + item.quantity, 0)}</strong>
              </div>
              <div className="shopping-cart-summary-row">
                <span>Subtotal</span>
                <strong>${subtotal.toFixed(2)}</strong>
              </div>
              <div className="shopping-cart-summary-row">
                <span>Shipping</span>
                <strong>{shipping === 0 ? 'Free' : `$${shipping.toFixed(2)}`}</strong>
              </div>
              <div className="shopping-cart-summary-row">
                <span>Estimated tax</span>
                <strong>${tax.toFixed(2)}</strong>
              </div>
              <div className="shopping-cart-summary-total">
                <span>Total</span>
                <strong>${total.toFixed(2)}</strong>
              </div>
              {cartItems.length > 0 && (
                <button
                  type="button"
                  className="shopping-cart-checkout-button"
                  onClick={() => setShowCheckout(!showCheckout)}
                >
                  {showCheckout ? 'Hide Checkout' : 'Check Out'}
                </button>
              )}
            </div>
          </aside>
        </div>

        {showCheckout && cartItems.length > 0 && (
          <div className="shopping-cart-checkout-section">
            <ShippingAddressForm />
            <CCInfoForm />
            <SubmitPurchaseInfoButton />
          </div>
        )}
      </section>
    </main>
  );
}