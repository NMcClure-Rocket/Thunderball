//import { useState, useEffect } from 'react';

interface OrderHistoryEntryProps {
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

export default function OrderHistoryEntry({ 
  itemid,
  name,
  description,
  format,
  potency,
  reusable,
  category,
  amount,
  transaction,
  purchase_time,
  delivery_est,
  imagelink
}: OrderHistoryEntryProps) {
  const baseURL = "http://localhost:8000";

  return (
    <div className="order-hist-entry">
      <div className="order-header-info">
        <label><strong>ORDER PLACED:</strong> {purchase_time}</label>
        <label><strong>TOTAL:</strong> ${transaction.toFixed(2)}</label>
        <label><strong>QUANTITY:</strong> {amount} item{amount !== 1 ? 's' : ''}</label>
      </div>

      <div className="order-body-info">
        <div className="order-image-section">
          <img 
            src={`${baseURL}${imagelink}`}
            alt={name}
            className="order-item-image"
          />
        </div>

        <div className="order-details-section">
          <h3>{name}</h3>
          <p>{description}</p>

          <div className="order-shipping-info">
            <label><strong>Estimated Delivery:</strong> {delivery_est}</label>
            <label><strong>Format:</strong> {format}</label>
            <label><strong>Potency:</strong> {potency}</label>
            <label><strong>Category:</strong> {category}</label>
            <label><strong>Reusable:</strong> {reusable === '1' ? 'Yes' : 'No'}</label>
          </div>
        </div>
      </div>
    </div>
  );
}