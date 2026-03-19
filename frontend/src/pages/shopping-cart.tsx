import { useState, useEffect } from 'react';
import CCInfoForm from '../components/forms/cc-info-form';
import ShippingAddressForm from '../components/forms/shipping-address-form';
import SubmitPurchaseInfoButton from '../components/buttons/submit-purchase-info-button';

import '../css/forms.css';
import shoppingCartTavern from '../assets/Shopping Cart Tavern.png';
import '../css/shopping-cart.css';

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

const placeholderCartItems: CartItem[] = [
  {
    itemId: 'placeholder-1',
    priceId: 'temp-1',
    name: 'Arc Lantern Serum',
    description: 'A bright, reusable tonic placeholder for the hero slot in your cart.',
    format: 'Glass Vial',
    potency: 3,
    reusable: true,
    category: 'Restoratives',
    price: '24.00',
    imageLink: '',
    quantity: 1,
  },
  {
    itemId: 'placeholder-2',
    priceId: 'temp-2',
    name: 'Field Kit Refill',
    description: 'A secondary line item to show stacking content and quantity controls.',
    format: 'Packet',
    potency: 2,
    reusable: false,
    category: 'Supplies',
    price: '12.50',
    imageLink: '',
    quantity: 2,
  },
  {
    itemId: 'placeholder-3',
    priceId: 'temp-3',
    name: 'Nightwatch Balm',
    description: 'A final placeholder product for summary and spacing behavior.',
    format: 'Tin',
    potency: 1,
    reusable: true,
    category: 'Recovery',
    price: '8.75',
    imageLink: '',
    quantity: 1,
  },
];

export default function ShoppingCart() {
  const [cartItems, setCartItems] = useState<CartItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [showShippingForm, setShowShippingForm] = useState(false);
  const [showCCForm, setShowCCForm] = useState(false);

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

  const displayItems = cartItems.length > 0 ? cartItems : placeholderCartItems;
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
            <span className="shopping-cart-kicker">Checkout staging area</span>
            <h1>Shopping Cart</h1>
            <p>
              A temporary cart layout with the content weighted to the right and
              enough structure to swap in real actions later.
            </p>
          </div>
          {isPreviewMode ? (
            <span className="shopping-cart-preview-badge">Preview placeholders</span>
          ) : (
            <span className="shopping-cart-preview-badge shopping-cart-preview-live">
              Live cart data
            </span>
          )}
        </header>

        <div className="shopping-cart-grid">
          <div className="shopping-cart-items">
            {displayItems.map((item, index) => (
              <article key={`${item.itemId}-${item.priceId}`} className="shopping-cart-card">
                <div className="shopping-cart-card-media">
                  <span>{item.category}</span>
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
                    <div className="shopping-cart-quantity-pill">
                      <button type="button" disabled>
                        -
                      </button>
                      <span>{item.quantity}</span>
                      <button type="button" disabled>
                        +
                      </button>
                    </div>
                    <button type="button" className="shopping-cart-text-button" disabled>
                      Save for later
                    </button>
                    <button type="button" className="shopping-cart-text-button" onClick={() => handleRemoveItem(index)} disabled={isPreviewMode}>
                      Remove
                    </button>
                  </div>
                </div>
              </article>
            ))}
          </div>

          <aside className="shopping-cart-summary">
            <div className="shopping-cart-summary-card">
              <h2>Order Summary</h2>
              <div className="shopping-cart-summary-row">
                <span>Items</span>
                <strong>{displayItems.length}</strong>
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
              <button type="button" className="shopping-cart-primary-button" disabled>
                Continue to checkout
              </button>
              <button type="button" className="shopping-cart-secondary-button" disabled>
                Apply promo code
              </button>
            </div>

            <div className="shopping-cart-note-card">
              <span className="shopping-cart-note-label">Temporary notes</span>
              <p>
                Use this block for shipping copy, loyalty messaging, or trust badges
                once the real checkout flow is ready.
              </p>
            </div>
          </aside>
        </div>
      </section>

      <div style={{ marginTop: '20px', marginBottom: '20px', padding: '15px', backgroundColor: '#f9f9f9', borderRadius: '8px' }}>
        <h3>Total Items: {cartItems.length}</h3>
        <h3>Total Price: ${total.toFixed(2)}</h3>
        <SubmitPurchaseInfoButton />
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
    </main>
  );
}