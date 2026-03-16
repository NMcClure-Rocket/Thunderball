import { useState, useEffect } from 'react';
import CatalogEntry from '../components/widgets/catalog-entry';
import AddToCart from '../components/widgets/add-to-cart';
import '../css/catalog.css';

interface Product {
  id: string;
  name: string;
  price: string;
  image: string;
}

export default function Catalog() {
  const [products, setProducts] = useState<Product[]>([]);
  const [selectedProductId, setSelectedProductId] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const baseURL = "http://127.0.0.1:8000";

   useEffect(() => {
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

        console.log(response);

        // Check if response is successful
        if (response.status === 200) {
          const data = await response.json();
          console.log("Success", data);
          
          // Map the response data to the Product interface
          setProducts(data.items);
        } else {
          setError('An error occurred. Please try again.');
        }
      } catch (err) {
        console.error('Error during GET request:', err);
        setError('Failed to connect to server');
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
  }, []);

  if (loading) {
    return <div>Loading products...</div>;
  }

  if (error) {
    return <div style={{ color: 'red' }}>Error: {error}</div>;
  }

  // // Placeholder data for now
  // const placeholderData: Product[] = [
  //   {
  //     id: '1',
  //     name: 'Product 1',
  //     price: '29.99',
  //     img: 'https://m.media-amazon.com/images/I/517OUyGVx0L._SY445_SX342_FMwebp_.jpg'
  //   },
  //   {
  //     id: '2',
  //     name: 'Product 2',
  //     price: '39.99',
  //     img: 'https://m.media-amazon.com/images/I/41JeHqPeF4L._SY445_SX342_FMwebp_.jpg'
  //   },
  //   {
  //     id: '3',
  //     name: 'Product 3',
  //     price: '49.99',
  //     img: 'https://m.media-amazon.com/images/I/51ME8NrcLjL._SY445_SX342_FMwebp_.jpg'
  //   },
  //   {
  //     id: '4',
  //     name: 'Product 4',
  //     price: '59.99',
  //     img: 'https://m.media-amazon.com/images/I/81IgjstJMmL._SY522_.jpg'
  //   },
  //   {
  //     id: '5',
  //     name: 'Product 5',
  //     price: '69.99',
  //     img: 'https://m.media-amazon.com/images/I/416A3fJ8nhL._SY445_SX342_FMwebp_.jpg'
  //   },
  //   {
  //     id: '6',
  //     name: 'Product 6',
  //     price: '79.99',
  //     img: 'https://m.media-amazon.com/images/I/517OUyGVx0L._SY445_SX342_FMwebp_.jpg'
  //   },
  //   {
  //     id: '7',
  //     name: 'Product 7',
  //     price: '89.99',
  //     img: 'https://m.media-amazon.com/images/I/41JeHqPeF4L._SY445_SX342_FMwebp_.jpg'
  //   },
  //   {
  //     id: '8',
  //     name: 'Product 8',
  //     price: '99.99',
  //     img: 'https://m.media-amazon.com/images/I/51ME8NrcLjL._SY445_SX342_FMwebp_.jpg'
  //   },
  //   {
  //     id: '9',
  //     name: 'Product 9',
  //     price: '10.99',
  //     img: 'https://m.media-amazon.com/images/I/51ME8NrcLjL._SY445_SX342_FMwebp_.jpg'
  //   },
  // ];


  // Split products into rows of 4
  const rows: Product[][] = [];
  for (let i = 0; i < products.length; i += 4) {
    rows.push(products.slice(i, i + 4));
  }

  const handleAddToCart = (cartItem: any) => {
    alert(`Added ${cartItem.name} to cart!`);
  };

  return (
    <div className="catalog-container">
      {rows.map((row, rowIndex) => (
        <div key={rowIndex} className="catalog-row">
          {row.map((product) => (
            <div
              key={product.id}
              onClick={() => setSelectedProductId(product.id)}
              style={{ cursor: 'pointer' }}
            >
              <CatalogEntry
                id={product.id}
                name={product.name}
                price={product.price}
                img={product.image}  // ← Map "image" to "img" prop
              />
            </div>
          ))}
        </div>
      ))}

      {selectedProductId && (
        <AddToCart
          priceId={selectedProductId}
          onClose={() => setSelectedProductId(null)}
          onAddToCart={handleAddToCart}
        />
      )}
    </div>
  );
}