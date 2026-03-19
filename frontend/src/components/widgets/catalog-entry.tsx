import { useState } from 'react';

function computeDeliveryDate(): string {
  const today = new Date();
  const randomDays = Math.floor(Math.random() * 15); // Random 0-14 days
  const date = new Date(today.getTime() + randomDays * 24 * 60 * 60 * 1000);
  return date.toLocaleDateString();
}

interface CatalogEntryProps {
  id: string;
  name: string;
  price: string;
  img: string;
}

export default function CatalogEntry({ id, name, price, img }: CatalogEntryProps) {
  const [deliveryDate] = useState(computeDeliveryDate);

  return (
    <div className="catalog-entry">
      <img src={img} alt={name} />
      {/* <h2>{id}</h2> */}
      <h2>{name}</h2>
      <h2>${price}</h2>
      <p>Estimated delivery: {deliveryDate}</p>
    </div>
  );
}