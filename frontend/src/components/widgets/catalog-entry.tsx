import { useState, useEffect } from 'react';

interface CatalogEntryProps {
  id: string;
  name: string;
  price: string;
  img: string;
}

export default function CatalogEntry({ id, name, price, img }: CatalogEntryProps) {
  const [deliveryDate, setDeliveryDate] = useState<string>('');

  // Generate random delivery date once when component mounts
  useEffect(() => {
    const today = new Date();
    const randomDays = Math.floor(Math.random() * 15); // Random 0-14 days
    const deliveryDate = new Date(today.getTime() + randomDays * 24 * 60 * 60 * 1000);
    setDeliveryDate(deliveryDate.toLocaleDateString());
  }, []);

  return (
    <div className="catalog-entry">
      <img src={img} alt={name} />
      <h2>{name}</h2>
      <h2>${price}</h2>
      <p>Estimated delivery: {deliveryDate}</p>
    </div>
  );
}