import { useState, useEffect } from 'react';
import CatalogEntry from '../components/widgets/catalog-entry';
import '../css/catalog.css';

interface Product {
  id: string;
  name: string;
  price: string;
  img: string;
}

export default function Catalog() {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);

  // Placeholder data for now
  const placeholderData: Product[] = [
    {
      id: '1',
      name: 'Product 1',
      price: '29.99',
      img: 'https://m.media-amazon.com/images/I/517OUyGVx0L._SY445_SX342_FMwebp_.jpg'
    },
    {
      id: '2',
      name: 'Product 2',
      price: '39.99',
      img: 'https://m.media-amazon.com/images/I/41JeHqPeF4L._SY445_SX342_FMwebp_.jpg'
    },
    {
      id: '3',
      name: 'Product 3',
      price: '49.99',
      img: 'https://m.media-amazon.com/images/I/51ME8NrcLjL._SY445_SX342_FMwebp_.jpg'
    },
    {
      id: '4',
      name: 'Product 4',
      price: '59.99',
      img: 'https://m.media-amazon.com/images/I/81IgjstJMmL._SY522_.jpg'
    },
    {
      id: '5',
      name: 'Product 5',
      price: '69.99',
      img: 'https://m.media-amazon.com/images/I/416A3fJ8nhL._SY445_SX342_FMwebp_.jpg'
    },
    {
      id: '6',
      name: 'Product 6',
      price: '79.99',
      img: 'https://m.media-amazon.com/images/I/517OUyGVx0L._SY445_SX342_FMwebp_.jpg'
    },
    {
      id: '7',
      name: 'Product 7',
      price: '89.99',
      img: 'https://m.media-amazon.com/images/I/41JeHqPeF4L._SY445_SX342_FMwebp_.jpg'
    },
    {
      id: '8',
      name: 'Product 8',
      price: '99.99',
      img: 'https://m.media-amazon.com/images/I/51ME8NrcLjL._SY445_SX342_FMwebp_.jpg'
    },
    {
      id: '9',
      name: 'Product 9',
      price: '10.99',
      img: 'https://m.media-amazon.com/images/I/51ME8NrcLjL._SY445_SX342_FMwebp_.jpg'
    },
  ];

  useEffect(() => {
    // TODO: Replace this with actual API call later
    // const fetchProducts = async () => {
    //   try {
    //     const response = await fetch('/api/products');
    //     const data = await response.json();
    //     setProducts(data);
    //   } catch (error) {
    //     console.error('Error fetching products:', error);
    //     setProducts(placeholderData);
    //   } finally {
    //     setLoading(false);
    //   }
    // };
    // fetchProducts();

    // For now, use placeholder data
    setProducts(placeholderData);
    setLoading(false);
  }, []);

  if (loading) {
    return <div>Loading products...</div>;
  }

  // Split products into rows of 4
  const rows: Product[][] = [];
  for (let i = 0; i < products.length; i += 4) {
    rows.push(products.slice(i, i + 4));
  }

  return (
    <div className="catalog-container">
      {rows.map((row, rowIndex) => (
        <div key={rowIndex} className="catalog-row">
          {row.map((product) => (
            <CatalogEntry
              key={product.id}
              id={product.id}
              name={product.name}
              price={product.price}
              img={product.img}
            />
          ))}
        </div>
      ))}
    </div>
  );
}