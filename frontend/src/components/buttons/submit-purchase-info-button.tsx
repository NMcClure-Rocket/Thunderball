import { useState } from 'react';

interface CartItem {
  itemId: string;
  priceId: string;
  name: string;
  description: string;
  format: string;
  potency: number;
  reusable: boolean;
  category: string;
  price: string;
  imageLink: string;
  quantity: number;
}

export default function SubmitPurchaseInfoButton() {
  const [loading, setLoading] = useState(false);
  const baseURL = "http://localhost:8000";

  const handleSubmitOrder = async () => {
    setLoading(true);
    console.log("=== PURCHASE SUBMIT START ===");

    // Get data from localStorage
    const cartJSON = localStorage.getItem('cart');
    const addressid = localStorage.getItem('addressid');
    const customerid = localStorage.getItem('customerid');
    const ccid = localStorage.getItem('ccid');

    console.log("Cart:", cartJSON);
    console.log("Address ID:", addressid);
    console.log("Customer ID:", customerid);
    console.log("CC ID:", ccid);

    if (!cartJSON || !addressid || !ccid || !customerid) {
      alert("Missing required information. Please complete shipping and payment forms.");
      setLoading(false);
      return;
    }

    try {
      const cartItems: CartItem[] = JSON.parse(cartJSON);

      // Build orders array from cart
      const orders = cartItems.map((item) => ({
        itemid: parseInt(item.itemId),
        qty: item.quantity,
        transaction: parseFloat(item.price) * item.quantity,
        customerid: parseInt(customerid),
        addressid: parseInt(addressid),
        ccid: parseInt(ccid)
      }));

      const requestBody = {
        orders: orders
      };

      console.log("Request Body:", requestBody);

      const response = await fetch(`${baseURL}/purchase`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestBody),
      });

      console.log("Response Status:", response.status);

      const data = await response.json();
      console.log("Response:", data);

      if (response.ok) {
        console.log("=== SUCCESS ===");
        alert("Order submitted successfully!");
        // Clear cart from localStorage
        localStorage.removeItem('cart');
      } else {
        console.log("=== FAILED ===");
        alert("Error submitting order");
      }
    } catch (err) {
      console.error('Error:', err);
      alert("Error submitting order");
    } finally {
      setLoading(false);
      console.log("=== PURCHASE SUBMIT END ===");
    }
  };

  return (
    <div>
      <button type="submit" onClick={handleSubmitOrder} disabled={loading}>
        {loading ? 'Processing...' : 'Submit Order'}
      </button>
    </div>
  );
}