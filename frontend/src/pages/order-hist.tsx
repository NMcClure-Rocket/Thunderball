import OrderHistoryEntry from '../components/widgets/order-hist-entry';
import '../css/order-hist.css';

export default function OrderHistory() {
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
