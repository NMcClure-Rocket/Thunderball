import { useState, useEffect } from 'react';
import CatalogEntry from '../components/widgets/catalog-entry';
import AddToCart from '../components/widgets/add-to-cart';
import rockyBackgroundImage from '../assets/RockyBG.png';
import '../css/catalog.css';

interface Product {
  id: number;
  name: string;
  price: number;
  image: string;
}

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

export default function Catalog() {
  const [products, setProducts] = useState<Product[]>([]);
  const [selectedProductId, setSelectedProductId] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const baseURL = "http://localhost:8000";

  useEffect(() => {
    document.body.classList.add('catalog-page');
    document.body.style.setProperty('--catalog-bg-image', `url('${rockyBackgroundImage}')`);

    const fetchProducts = async () => {
      setError('');
      setLoading(true);

      try {
        const response = await fetch(`${baseURL}/inventory`, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        });

        if (response.status === 200) {
          let data = await response.json();
          console.log("Raw response:", data);
          data = JSON.parse(data);
          
          // Extract items from the response object
          const productArray = data.items && Array.isArray(data.items) ? data.items : [];
          console.log("Products array:", productArray);
          
          setProducts(productArray);
        } else {
          setError('Failed to load products');
        }
      } catch (err) {
        console.error('Error during GET request:', err);
        setError('Failed to connect to server');
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();

    return () => {
      document.body.classList.remove('catalog-page');
      document.body.style.removeProperty('--catalog-bg-image');
    };
  }, []);

  if (loading) {
    return <div>Loading products...</div>;
  }

  if (error) {
    return <div style={{ color: 'red' }}>Error: {error}</div>;
  }

  if (products.length === 0) {
    return <div>No products available</div>;
  }

  // Split products into rows of 4
  const rows: Product[][] = [];
  for (let i = 0; i < products.length; i += 4) {
    rows.push(products.slice(i, i + 4));
  }

  const handleAddToCart = (cartItem: Product) => {
    alert(`Added ${cartItem.name} to cart!`);
  };

  return (
    <div className="catalog-container">
      {rows.map((row, rowIndex) => (
        <div key={rowIndex} className="catalog-row">
          {row.map((product) => (
            <div
              key={product.id}
              onClick={() => setSelectedProductId(product.id.toString())}
              style={{ cursor: 'pointer' }}
            >
              <CatalogEntry
                id={product.id.toString()}
                name={product.name}
                price={product.price.toString()}
                img={product.image}
              />
            </div>
          ))}
        </div>
      ))}

      {selectedProductId && (
        <AddToCart
          priceId={selectedProductId}
          onClose={() => setSelectedProductId(null)}
          onAddToCart={handleAddToCart as unknown as (cartItem: CartItem) => void}
        />
      )}
    </div>
  );
}