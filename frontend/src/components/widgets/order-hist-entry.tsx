import { useState, useEffect } from 'react';

interface OrderHistoryEntryProps {
  orderId: string;
}

export default function OrderHistoryEntry({ orderId }: OrderHistoryEntryProps) {
  const [deliveryDate, setDeliveryDate] = useState<string>('');
  const [amount, setAmount] = useState<string>('');
  const [custName, setCustName] = useState<string>('');
  const [address, setAddress] = useState<string>('');
  const [quantity, setQuantity] = useState<string>('');

  const fnames = ["Sam", "Joe", "Tom", "Matthew", "Trevor", "Fred"];
  const lnames = ["Darnold", "Flacco", "Brady", "Stafford", "Lawrence", "Tagovailoa"];

  const streets = ["Main St", "Oak Ave", "Elm Street", "Pine Road", "Maple Drive", "Cedar Lane"];
  const cities = ["Springfield", "Shelbyville", "Capital City", "Gotham", "Metropolis", "Smallville"];
  const states = ["AZ", "CA", "TX", "FL", "NY", "IL", "PA", "OH", "GA", "NC"];

  // Function to generate random address
  const generateRandomAddress = (): string => {
    const randomStreetNum = Math.floor(Math.random() * 9000) + 1000;
    const randomStreet = streets[Math.floor(Math.random() * streets.length)];
    const randomCity = cities[Math.floor(Math.random() * cities.length)];
    const randomState = states[Math.floor(Math.random() * states.length)];
    const randomZip = Math.floor(Math.random() * 90000) + 10000;

    return `${randomStreetNum} ${randomStreet}, ${randomCity}, ${randomState} ${randomZip}, USA`;
  };

  useEffect(() => {
    // Generate random customer name
    const randomFnameIndex = Math.floor(Math.random() * fnames.length);
    const randomLnameIndex = Math.floor(Math.random() * lnames.length);
    const fullName = fnames[randomFnameIndex] + " " + lnames[randomLnameIndex];
    setCustName(fullName);

    // Generate random amount
    const baseAmount = 10.00;
    const randomExtra = Math.floor(Math.random() * 90);
    const totalAmount = baseAmount + randomExtra;
    setAmount(totalAmount.toString());

    // Generate delivery date
    const today = new Date();
    setDeliveryDate(today.toLocaleDateString());

    // Generate random address
    setAddress(generateRandomAddress());

    // Generate random quantity (1-10 items)
    const randomQuantity = Math.floor(Math.random() * 10) + 1;
    setQuantity(randomQuantity.toString());
  }, []);

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