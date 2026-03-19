import { useState, useEffect } from 'react';
import OrderHistoryEntry from '../components/widgets/order-hist-entry';
import '../css/order-hist.css';

interface OrderItem {
  itemid: number;
  name: string;
  description: string;
  format: string;
  potency: number;
  reusable: string;
  category: string;
  amount: number;
  transaction: number;
  purchase_time: string;
  delivery_est: string;
  imagelink: string;
}

export default function OrderHistory() {
  const [orders, setOrders] = useState<OrderItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const baseURL = "http://localhost:8000";

  useEffect(() => {
    const fetchOrders = async () => {
      setError('');
      setLoading(true);

      try {
        // Get customerid from localStorage
        const customerId = localStorage.getItem('customerid');
        
        if (!customerId) {
          setError('Customer ID not found. Please log in.');
          setLoading(false);
          return;
        }

        console.log("Fetching orders for customerid:", customerId);

        const response = await fetch(`${baseURL}/orders/${customerId}`, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        });

        console.log("Response status:", response.status);

        if (response.ok) {
          let data = await response.json();
          console.log("Raw response:", data);

          // Handle double-encoded JSON if needed
          if (typeof data === 'string') {
            data = JSON.parse(data);
          }

          // Extract rows from response
          const orderItems = data.rows && Array.isArray(data.rows) ? data.rows : [];
          console.log("Orders array:", orderItems);

          setOrders(orderItems);
        } else {
          setError('Failed to load orders');
        }
      } catch (err) {
        console.error('Error fetching orders:', err);
        setError('Failed to connect to server');
      } finally {
        setLoading(false);
      }
    };

    fetchOrders();
  }, []);

  if (loading) {
    return <div className="order-history-container"><h1>Loading orders...</h1></div>;
  }

  if (error) {
    return <div className="order-history-container"><h1>{error}</h1></div>;
  }

  if (orders.length === 0) {
    return <div className="order-history-container"><h1>No orders found</h1></div>;
  }

  return (
    <div className="order-history-container">
      <h1>Order History</h1>
      <div className="order-history-list">
        {orders.map((order) => (
          <OrderHistoryEntry 
            key={order.itemid}
            itemid={order.itemid}
            name={order.name}
            description={order.description}
            format={order.format}
            potency={order.potency}
            reusable={order.reusable}
            category={order.category}
            amount={order.amount}
            transaction={order.transaction}
            purchase_time={order.purchase_time}
            delivery_est={order.delivery_est}
            imagelink={order.imagelink}
          />
        ))}
      </div>
    </div>
  );
}
