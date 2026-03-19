import { useState } from 'react';
import React from 'react';
import '../../css/add-to-cart.css';

interface AddToCartProps {
  priceId: string;
  onClose: () => void;
  onAddToCart: (cartItem: CartItem) => void;
}

export interface CartItem {
  itemId: string;
  //priceId: string;
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

interface BasePriceItem {
  id: number;
  name: string;
  price: number;
  image: string;
}

interface InventoryItem {
  itemid: number;
  name: string;
  description: string;
  format: string;
  potency: number;
  reusable: string;
  category: string;
  price: number;
  amount: number;
  base_info: number;
}

export default function AddToCart({ priceId, onClose, onAddToCart }: AddToCartProps) {
  const [baseItem, setBaseItem] = useState<BasePriceItem | null>(null);
  const [inventoryItems, setInventoryItems] = useState<InventoryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [quantity, setQuantity] = useState(1);
  
  // New state for filter selections
  const [selectedReusable, setSelectedReusable] = useState<boolean | null>(null);
  const [selectedFormat, setSelectedFormat] = useState<string | null>(null);
  const [selectedPotency, setSelectedPotency] = useState<number | null>(null);
  
  const baseURL = "http://localhost:8000";

  // Fetch from Inventory table only
  React.useEffect(() => {
    const fetchData = async () => {
      setError('');
      setLoading(true);

      try {
        const response = await fetch(`${baseURL}/inventory/${priceId}`, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        });

        if (!response.ok) {
          throw new Error('Failed to fetch inventory');
        }

        let data = await response.json();
        console.log("Inventory data:", data);
        data = JSON.parse(data);

        // Handle different response formats
        let items = [];
        if (Array.isArray(data)) {
          items = data;
        } else if (data.items && Array.isArray(data.items)) {
          items = data.items;
        } else if (data.rows && Array.isArray(data.rows)) {
          items = data.rows;  // ✅ Handle {"rows": [...]} format
        }
        //const items = Array.isArray(data) ? data : (data.items || []);
        console.log("Items array:", items);
        
        if (items.length === 0) {
          setError('No inventory available');
          setLoading(false);
          return;
        }

        setBaseItem({
          id: items[0].base_info,
          name: items[0].name,
          price: items[0].price,
          image: "placeholder.png"
        });

        setInventoryItems(items);
      } catch (err) {
        console.error('Error fetching inventory:', err);
        setError('Failed to load product details');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [priceId]);

  // Get formats based on selected reusable status
  const availableFormats = selectedReusable !== null
    ? Array.from(new Set(
        inventoryItems
          .filter(item => (item.reusable === '1' || item.reusable === 'true') === selectedReusable)
          .map(item => item.format)
      ))
    : [];

  // Get potencies based on selected reusable and format
  const availablePotencies = selectedFormat !== null
    ? Array.from(new Set(
        inventoryItems
          .filter(item => 
            ((item.reusable === '1' || item.reusable === 'true') === selectedReusable) &&
            item.format === selectedFormat
          )
          .map(item => item.potency)
      )).sort((a, b) => a - b)
    : [];

  // Get the selected item based on all filters
  const selectedItem = inventoryItems.find(item =>
    ((item.reusable === '1' || item.reusable === 'true') === selectedReusable) &&
    item.format === selectedFormat &&
    item.potency === selectedPotency
  ) || null;

  const handleAddToCart = () => {
    if (!selectedItem || !baseItem) {
      alert('Please select all options');
      return;
    }

    // Check if enough inventory is available
    if (quantity > selectedItem.amount) {
      alert(`Only ${selectedItem.amount} items available in stock`);
      return;
    }

    const cartItem: CartItem = {
      itemId: selectedItem.itemid.toString(),
      //priceId: baseItem.id.toString(),
      name: selectedItem.name,
      description: selectedItem.description,
      format: selectedItem.format,
      potency: selectedItem.potency,
      reusable: selectedItem.reusable === '1' || selectedItem.reusable === 'true',
      category: selectedItem.category,
      price: selectedItem.price.toString(),
      imageLink: baseItem.image,
      quantity
    };

    // Save to local storage
    const existingCart = JSON.parse(localStorage.getItem('cart') || '[]');
    existingCart.push(cartItem);
    localStorage.setItem('cart', JSON.stringify(existingCart));

    onAddToCart(cartItem);
    onClose();
  };

  if (loading) {
    return (
      <div className="modal-overlay" onClick={onClose}>
        <div className="modal-content" onClick={(e) => e.stopPropagation()}>
          <div>Loading product...</div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="modal-overlay" onClick={onClose}>
        <div className="modal-content" onClick={(e) => e.stopPropagation()}>
          <div style={{ color: 'red' }}>{error}</div>
          <button onClick={onClose} style={{ marginTop: '15px', padding: '10px 20px' }}>
            Close
          </button>
        </div>
      </div>
    );
  }

  if (!baseItem || inventoryItems.length === 0) {
    return (
      <div className="modal-overlay" onClick={onClose}>
        <div className="modal-content" onClick={(e) => e.stopPropagation()}>
          <div>No inventory available for this product</div>
        </div>
      </div>
    );
  }

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <button className="close-button" onClick={onClose}>✕</button>

        <div className="modal-body">
          <div className="modal-image">
            <img src={baseItem.image} alt={baseItem.name} />
          </div>

          <div className="modal-details">
            <h2>{baseItem.name}</h2>
            {baseItem && (
              <p className="description">Base Price: ${baseItem.price}</p>
            )}

            {/* Reusable Checkbox */}
            <div className="form-group">
              <label>Spell Type:</label>
              <div className="reusable-options">
                {inventoryItems.some(item => (item.reusable === '1' || item.reusable === 'true')) && (
                  <label>
                    <input
                      type="radio"
                      name="spellType"
                      checked={selectedReusable === true}
                      onChange={() => {
                        setSelectedReusable(true);
                        setSelectedFormat(null);
                        setSelectedPotency(null);
                      }}
                    />
                    Reusable
                  </label>
                )}
                {inventoryItems.some(item => (item.reusable === '0' || item.reusable === 'false')) && (
                  <label>
                    <input
                      type="radio"
                      name="spellType"
                      checked={selectedReusable === false}
                      onChange={() => {
                        setSelectedReusable(false);
                        setSelectedFormat(null);
                        setSelectedPotency(null);
                      }}
                    />
                    Single Use
                  </label>
                )}
              </div>
            </div>

            {/* Format Dropdown */}
            <div className="form-group">
              <label>Format:</label>
              <select
                value={selectedFormat || ''}
                onChange={(e) => {
                  setSelectedFormat(e.target.value || null);
                  setSelectedPotency(null);
                }}
                disabled={selectedReusable === null}
              >
                <option value="">Select a format</option>
                {availableFormats.map((format) => (
                  <option key={format} value={format}>
                    {format}
                  </option>
                ))}
              </select>
              {selectedReusable === null && (
                <p style={{ fontSize: '0.9em', color: '#666' }}>Please select a spell type first</p>
              )}
            </div>

            {/* Potency Dropdown */}
            <div className="form-group">
              <label>Potency:</label>
              <select
                value={selectedPotency || ''}
                onChange={(e) => setSelectedPotency(parseInt(e.target.value) || null)}
                disabled={selectedFormat === null}
              >
                <option value="">Select a potency</option>
                {availablePotencies.map((potency) => (
                  <option key={potency} value={potency}>
                    {potency}
                  </option>
                ))}
              </select>
              {selectedFormat === null && (
                <p style={{ fontSize: '0.9em', color: '#666' }}>Please select a format first</p>
              )}
            </div>

            {/* Display selected item details */}
            {selectedItem && (
              <div className="selected-item-summary">
                <p><strong>Selected:</strong> {selectedItem.format} • Potency {selectedItem.potency} • {selectedItem.reusable === '1' || selectedItem.reusable === 'true' ? 'Reusable' : 'Single Use'}</p>
                <p><strong>Price per unit:</strong> ${selectedItem.price.toFixed(2)}</p>
                <p><strong>Stock available:</strong> {selectedItem.amount}</p>
              </div>
            )}

            {/* Quantity Input */}
            {selectedItem && (
              <div className="form-group">
                <label>Quantity:</label>
                <input
                  type="number"
                  value={quantity}
                  onChange={(e) => setQuantity(parseInt(e.target.value) || 1)}
                  min="1"
                  max={selectedItem.amount}
                />
                {quantity > selectedItem.amount && (
                  <span className="error-text">Quantity exceeds available stock</span>
                )}
              </div>
            )}

            {/* Total Price */}
            {selectedItem && (
              <div className="total-price">
                <strong>Total: ${(selectedItem.price * quantity).toFixed(2)}</strong>
              </div>
            )}

            {/* Add to Cart Button */}
            <button 
              className="add-to-cart-btn" 
              onClick={handleAddToCart}
              disabled={!selectedItem || quantity > selectedItem.amount || selectedItem.amount === 0}
            >
              Add to Cart
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}