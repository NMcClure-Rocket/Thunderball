import { useState } from 'react';

interface SubmitCCInfoFormButtonProps {
  cardholderFName: string;
  cardholderLName: string;
  processor: string;
  cardNumber: string;
  expiration: string;
  cvc: string;
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


    const requestBody = {
      number: parseInt(cardNumber),
      security_code: parseInt(cvc),
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

    console.log("Submitting:", requestBody);

    try {
      const response = await fetch(`${baseURL}/newcc`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestBody),
      });

      const data = await response.json();
      console.log("Response:", data);
      // Save ccid from response data in local Storage
      if (data.ccid) {
        if (data.ccid) {
          localStorage.setItem('ccid', data.ccid.toString());
          console.log("Saved ccid:", data.ccid);
        }
      }
      if (response.ok) {
        alert("Credit card information successfully saved!");
      } 
    } catch (err) {
      console.error('Error:', err);
      alert("Error submitting credit card information");
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