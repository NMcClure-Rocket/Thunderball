import { useState, useEffect } from 'react';
import OrderHistoryEntry from '../components/widgets/order-hist-entry';
import '../css/order-hist.css';

export default function OrderHistory() {
  const [deliveryDate, setDeliveryDate] = useState<string>('');
  const [amount, setAmount] = useState<string>('');
  const [custName, setCustName] = useState<string>('');
  const [address, setAddress] = useState<string>('');

  const fnames = ["Sam", "Joe", "Tom", "Matthew", "Trevor"];
  const lnames = ["Darnold", "Flacco", "Brady", "Stafford", "Lawrence"];

  const streets = ["Main St", "Oak Ave", "Elm Street", "Pine Road", "Maple Drive", "Cedar Lane"];
  const cities = ["Springfield", "Shelbyville", "Capital City", "Gotham", "Metropolis", "Smallville"];
  const states = ["AZ", "CA", "TX", "FL", "NY", "IL", "PA", "OH", "GA", "NC"];

  // Function to generate random address
  const generateRandomAddress = (): string => {
    const randomStreetNum = Math.floor(Math.random() * 9000) + 1000; // 1000-10000
    const randomStreet = streets[Math.floor(Math.random() * streets.length)];
    const randomCity = cities[Math.floor(Math.random() * cities.length)];
    const randomState = states[Math.floor(Math.random() * states.length)];
    const randomZip = Math.floor(Math.random() * 90000) + 10000; // 10000-99999

    return `${randomStreetNum} ${randomStreet}, ${randomCity}, ${randomState} ${randomZip}, USA`;
  };

  // One useEffect that does everything
  useEffect(() => {
    // Generate random customer name
    const randomFnameIndex = Math.floor(Math.random() * fnames.length);
    const randomLnameIndex = Math.floor(Math.random() * lnames.length);
    const fullName = fnames[randomFnameIndex] + " " + lnames[randomLnameIndex];
    setCustName(fullName);

    // Generate random amount
    const baseAmount = 10.00;
    const randomExtra = Math.floor(Math.random() * 10);
    const totalAmount = baseAmount + randomExtra;
    setAmount(totalAmount.toString());

    // Generate delivery date
    const today = new Date();
    setDeliveryDate(today.toLocaleDateString());

    // Generate random address
    setAddress(generateRandomAddress());
  }, []); // Empty array = runs once when component loads

  // Sample order IDs in reverse chronological order (newest first)
  const orderIds = ['ORD-2026-00005', 'ORD-2026-00004', 'ORD-2026-00003', 'ORD-2026-00002', 'ORD-2026-00001'];

  return (
    <div className="order-history-container">
      <h1>Order History</h1>
      <div className="order-history-list">
        {orderIds.map((orderId) => (
          <OrderHistoryEntry key={orderId} orderId={orderId} />
        ))}
      </div>
    </div>
  );
}
