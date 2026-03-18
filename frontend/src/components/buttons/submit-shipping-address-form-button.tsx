import { useState } from 'react';

interface SubmitShippingAddressFormButtonProps {
    fName: string;
    lName: string;
    address: string;
    address2: string;
    city: string;
    state: string;
    country: string;
    zip: string;
    customerId: number
}

export default function SubmitShippingAddressFormButton({
    fName,
    lName,
    address,
    address2,
    city,
    state,
    country,
    zip,
    customerId

}: SubmitShippingAddressFormButtonProps) {
    const [loading, setLoading] = useState(false);
    const baseURL = "http://localhost:8000";

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
    setLoading(true);


    const requestBody = {
      first_name: fName,
      last_name: lName,
      address: address,
      addr_2: address2,
      city: city,
      state: state,
      country: country,
      zip: zip,
      customerid: customerId
    };

    console.log("Submitting:", requestBody);

    try {
      const response = await fetch(`${baseURL}/newaddress`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestBody),
      });

      const data = await response.json();
      console.log("Response:", data);
    if (response.ok) {
        alert("Shipping address information successfully saved!");
      } 
    } catch (err) {
      console.error('Error:', err);
      alert("Error submitting shippting address information");
    } finally {
      setLoading(false);
    }

    };
    return (
    <button type="submit" onClick={handleSubmit} disabled={loading}>
      {loading ? 'Processing...' : 'Submit'}
    </button>
  );
}