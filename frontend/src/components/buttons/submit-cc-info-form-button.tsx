import { useState } from 'react';

interface SubmitCCInfoFormButtonProps {
  cardholderFName: string;
  cardholderLName: string;
  processor: string;
  cardNumber: number;
  expiration: string;
  cvc: number;
  address: string;
  address2: string;
  city: string;
  state: string;
  country: string;
  zip: string;
  customerId: number;
}

export default function SubmitCCInfoFormButton({
  cardholderFName,
  cardholderLName,
  processor,
  cardNumber,
  expiration,
  cvc,
  address,
  address2,
  city,
  state,
  country,
  zip,
  customerId
}: SubmitCCInfoFormButtonProps) {
  const [loading, setLoading] = useState(false);
  const baseURL = "http://localhost:8000";

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    console.log("=== SUBMIT START ===");

    const requestBody = {
      number: cardNumber,
      security_code: cvc,
      expiration: expiration,
      processor: processor,
      first_name: cardholderFName,
      last_name: cardholderLName,
      address: address,
      addr_2: address2,
      city: city,
      state: state,
      country: country,
      zip: zip,
      customerid: customerId
    };

    console.log("Request Body:", requestBody);
    console.log("All fields present:", {
      number: !!cardNumber,
      security_code: !!cvc,
      expiration: !!expiration,
      processor: !!processor,
      first_name: !!cardholderFName,
      last_name: !!cardholderLName,
      address: !!address,
      addr_2: !!address2,
      city: !!city,
      state: !!state,
      country: !!country,
      zip: !!zip,
      customerid: !!customerId
    });

    try {
      
      const response = await fetch(`${baseURL}/newcc`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestBody),
      });

      console.log("Response Status:", response.status);
      
      const data = await response.json();
      console.log("Response Data:", data);
      console.log("Response Detail:", data.detail);
      
      if (data.detail && Array.isArray(data.detail)) {
        console.log("Missing/Invalid Field:");
        data.detail.forEach((err: { type: string; loc: string[]; msg: string }) => {
          console.log("  - Type:", err.type);
          console.log("  - Location:", err.loc);
          console.log("  - Message:", err.msg);
        });
      }

      if (data.ccid) {
        localStorage.setItem('ccid', data.ccid.toString());
        console.log("Saved ccid:", data.ccid);
      }

      if (response.ok) {
        if (data.customerid) {
          localStorage.setItem('addressid', data.customerid.toString());
          console.log("Saved addressid:", data.customerid);
        }
        alert("Credit card information successfully saved!");
      } else {
        console.log("=== FAILED ===");
        alert("Error submitting credit card information");
      }
    } catch (err) {
      console.error('Error:', err);
      alert("Error submitting credit card information");
    } finally {
      setLoading(false);
      console.log("=== SUBMIT END ===");
    }
  };

  return (
    <button type="submit" onClick={handleSubmit} disabled={loading}>
      {loading ? 'Processing...' : 'Submit'}
    </button>
  );
}