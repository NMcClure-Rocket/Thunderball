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

interface BasePriceItem {
  priceId: number;
  item: string;
  price: string;
  imageLink: string;
}

interface InventoryItem {
  itemId: string;
  name: string;
  description: string;
  format: string;
  potency: number;
  reusable: boolean;
  category: string;
  price: string;
  amount: number;
  baseInfo: number;
}

export default function AddToCart({ priceId, onClose, onAddToCart }: AddToCartProps) {
  const [baseItem, setBaseItem] = useState<BasePriceItem | null>(null);
  const [inventoryItems, setInventoryItems] = useState<InventoryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [quantity, setQuantity] = useState(1);
  const [selectedItemId, setSelectedItemId] = useState<string>('');

  // Placeholder data - replace with API calls
  const placeholderBasePrice: { [key: string]: BasePriceItem } = {
    '1': {
      priceId: 1,
      item: 'Shield',
      price: '49.99',
      imageLink: 'https://m.media-amazon.com/images/I/517OUyGVx0L._SY445_SX342_FMwebp_.jpg'
    },
    '2': {
      priceId: 2,
      item: 'Attack',
      price: '29.99',
      imageLink: 'https://m.media-amazon.com/images/I/41JeHqPeF4L._SY445_SX342_FMwebp_.jpg'
    },
    '3': {
      priceId: 3,
      item: 'Focus',
      price: '45.99',
      imageLink: 'https://m.media-amazon.com/images/I/51ME8NrcLjL._SY445_SX342_FMwebp_.jpg'
    },
  };

  const placeholderInventory: { [key: string]: InventoryItem[] } = {
    '1': [
      {
        itemId: '001',
        name: 'Shield',
        description: 'hello world',
        format: 'Online PDF',
        potency: 58,
        reusable: true,
        category: 'Protection',
        price: '49.99',
        amount: 20,
        baseInfo: 1
      },
      {
        itemId: '002',
        name: 'Shield',
        description: 'hello world',
        format: 'Online PDF',
        potency: 58,
        reusable: false,
        category: 'Protection',
        price: '45.99',
        amount: 15,
        baseInfo: 1
      },
      {
        itemId: '003',
        name: 'Shield',
        description: 'hello world',
        format: 'Hard Cover',
        potency: 42,
        reusable: false,
        category: 'Protection',
        price: '55.99',
        amount: 3,
        baseInfo: 1
      },
      {
        itemId: '004',
        name: 'Shield',
        description: 'hello world',
        format: 'Hard Cover',
        potency: 41,
        reusable: false,
        category: 'Protection',
        price: '56.99',
        amount: 7,
        baseInfo: 1
      },
    ],
    '2': [
      {
        itemId: '005',
        name: 'Attack',
        description: 'hello world',
        format: 'Online PDF',
        potency: 22,
        reusable: true,
        category: 'Attack',
        price: '45.99',
        amount: 15,
        baseInfo: 2
      },
    ],
  };

  // Fetch base price item and inventory items
  React.useEffect(() => {
    // TODO: Replace with actual API calls
    // const fetchData = async () => {
    //   try {
    //     // Fetch base price info
    //     const basePriceResponse = await fetch(`/api/base-price/${priceId}`);
    //     const basePriceData = await basePriceResponse.json();
    //     setBaseItem(basePriceData);
    //
    //     // Fetch inventory items with this priceId as FK (base_info)
    //     const inventoryResponse = await fetch(`/api/inventory/base-price/${priceId}`);
    //     const inventoryData = await inventoryResponse.json();
    //     setInventoryItems(inventoryData);
    //     
    //     if (inventoryData.length > 0) {
    //       setSelectedItemId(inventoryData[0].itemId);
    //     }
    //   } catch (error) {
    //     console.error('Error fetching data:', error);
    //   } finally {
    //     setLoading(false);
    //   }
    // };
    // fetchData();

    // For now, use placeholder data
    const baseItemData = placeholderBasePrice[priceId];
    const inventoryData = placeholderInventory[priceId] || [];

    if (baseItemData) {
      setBaseItem(baseItemData);
    }

    if (inventoryData.length > 0) {
      setInventoryItems(inventoryData);
      setSelectedItemId(inventoryData[0].itemId);
    }

    setLoading(false);
  }, [priceId]);

  const selectedItem = inventoryItems.find(item => item.itemId === selectedItemId);

  const handleAddToCart = () => {
    if (!selectedItem || !baseItem) return;

    // Check if enough inventory is available
    if (quantity > selectedItem.amount) {
      alert(`Only ${selectedItem.amount} items available in stock`);
      return;
    }

    const cartItem: CartItem = {
      itemId: selectedItem.itemId,
      priceId: baseItem.priceId.toString(),
      name: selectedItem.name,
      description: selectedItem.description,
      format: selectedItem.format,
      potency: selectedItem.potency,
      reusable: selectedItem.reusable,
      category: selectedItem.category,
      price: selectedItem.price,
      imageLink: baseItem.imageLink,
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
            <img src={baseItem.imageLink} alt={baseItem.item} />
          </div>

          <div className="modal-details">
            <h2>{baseItem.item}</h2>
            {selectedItem && (
              <p className="description">{selectedItem.description}</p>
            )}

            <div className="form-group">
              <label>Available Options:</label>
              <div className="inventory-options">
                {inventoryItems.map((item) => (
                  <button
                    key={item.itemId}
                    className={`inventory-option ${selectedItemId === item.itemId ? 'selected' : ''} ${item.amount === 0 ? 'out-of-stock' : ''}`}
                    onClick={() => setSelectedItemId(item.itemId)}
                    disabled={item.amount === 0}
                  >
                    <div className="option-details">
                      <span className="format">{item.format}</span>
                      <span className="potency">Potency: {item.potency}</span>
                      <span className="reusable">{item.reusable ? '♻️ Reusable' : 'Single Use'}</span>
                      <span className="stock">
                        {item.amount > 0 ? `${item.amount} in stock` : 'Out of Stock'}
                      </span>
                    </div>
                    <div className="option-price">${item.price}</div>
                  </button>
                ))}
              </div>
            </div>

            {selectedItem && (
              <div className="selected-item-summary">
                <p><strong>Selected:</strong> {selectedItem.format} • Potency {selectedItem.potency} • {selectedItem.reusable ? 'Reusable' : 'Single Use'}</p>
                <p><strong>Price per unit:</strong> ${selectedItem.price}</p>
                <p><strong>Stock available:</strong> {selectedItem.amount}</p>
              </div>
            )}

            <div className="form-group">
              <label>Quantity:</label>
              <input
                type="number"
                value={quantity}
                onChange={(e) => setQuantity(parseInt(e.target.value) || 1)}
                min="1"
                max={selectedItem?.amount || 1}
              />
              {selectedItem && quantity > selectedItem.amount && (
                <span className="error-text">Quantity exceeds available stock</span>
              )}
            </div>

            {selectedItem && (
              <div className="total-price">
                <strong>Total: ${(parseFloat(selectedItem.price) * quantity).toFixed(2)}</strong>
              </div>
            )}

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