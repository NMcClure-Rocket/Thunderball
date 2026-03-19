import { useState } from 'react';

interface OrderHistoryEntryProps {
  orderId: string;
}

const fnames = ["Sam", "Joe", "Tom", "Matthew", "Trevor", "Fred"];
const lnames = ["Darnold", "Flacco", "Brady", "Stafford", "Lawrence", "Tagovailoa"];
const streets = ["Main St", "Oak Ave", "Elm Street", "Pine Road", "Maple Drive", "Cedar Lane"];
const cities = ["Springfield", "Shelbyville", "Capital City", "Gotham", "Metropolis", "Smallville"];
const states = ["AZ", "CA", "TX", "FL", "NY", "IL", "PA", "OH", "GA", "NC"];

function generateRandomAddress(): string {
  const randomStreetNum = Math.floor(Math.random() * 9000) + 1000;
  const randomStreet = streets[Math.floor(Math.random() * streets.length)];
  const randomCity = cities[Math.floor(Math.random() * cities.length)];
  const randomState = states[Math.floor(Math.random() * states.length)];
  const randomZip = Math.floor(Math.random() * 90000) + 10000;
  return `${randomStreetNum} ${randomStreet}, ${randomCity}, ${randomState} ${randomZip}, USA`;
}

function computeCustName(): string {
  const i = Math.floor(Math.random() * fnames.length);
  const j = Math.floor(Math.random() * lnames.length);
  return fnames[i] + " " + lnames[j];
}

function computeAmount(): string {
  return (10 + Math.floor(Math.random() * 90)).toString();
}

function computeQuantity(): string {
  return (Math.floor(Math.random() * 10) + 1).toString();
}

function computeDeliveryDate(): string {
  return new Date().toLocaleDateString();
}

export default function OrderHistoryEntry({ orderId }: OrderHistoryEntryProps) {
  const [deliveryDate] = useState(computeDeliveryDate);
  const [custName] = useState(computeCustName);
  const [amount] = useState(computeAmount);
  const [address] = useState(generateRandomAddress);
  const [quantity] = useState(computeQuantity);

  return (
    <div className="order-hist-entry">
      <div className="order-header-info">
        <label><strong>ORDER ID:</strong> {orderId}</label>
        <label><strong>ORDER PLACED:</strong> {deliveryDate}</label>
        <label><strong>TOTAL:</strong> ${amount}</label>
        <label><strong>QUANTITY:</strong> {quantity} items</label>
      </div>

      <div className="order-body-info">
        <div className="order-image-section">
          <img 
            src="https://m.media-amazon.com/images/I/517OUyGVx0L._SY445_SX342_FMwebp_.jpg" 
            alt="Order item"
            className="order-item-image"
          />
        </div>

        <div className="order-details-section">
          <h3>Product Name</h3>
          <p>Product Description goes here. This is a brief description of the product ordered.</p>

          <div className="order-shipping-info">
            <label><strong>Delivered:</strong> {deliveryDate}</label>
            <label><strong>Shipped to:</strong> {custName}</label>
            <label>{address}</label>
          </div>
        </div>
      </div>
    </div>
  );
}