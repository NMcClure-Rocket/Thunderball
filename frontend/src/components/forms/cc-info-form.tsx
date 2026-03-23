import { useState } from 'react';
import SubmitCCInfoFormButton from "../buttons/submit-cc-info-form-button";
import USStatesDropdown from "../dropdowns/US-states-dropdown";

export default function CCInfoForm() {
  const [cardholderFName, setCardholderFName] = useState('');
  const [cardholderLName, setCardholderLName] = useState('');
  const [email, setEmail] = useState('');
  const [processor, setProcessor] = useState('Visa');
  const [cardNumber, setCardNumber] = useState('');
  const [expiration, setExpiration] = useState('');
  const [cvc, setCvc] = useState('');
  const [address, setAddress] = useState('');
  const [address2, setAddress2] = useState('');
  const [city, setCity] = useState('');
  const [state, setState] = useState('');
  const [country, setCountry] = useState('');
  const [zip, setZip] = useState('');
  const [customerId] = useState(() => localStorage.getItem('customerid') ?? '');

  return (
    <div className="shipping-form-wrapper">
      <h1>Credit Card Checkout Form</h1>
      <form>
        <label>Cardholder First Name</label>
        <input type="text" value={cardholderFName} onChange={(e) => setCardholderFName(e.target.value)} />
        <label>Cardholder Last Name</label>
        <input type="text" value={cardholderLName} onChange={(e) => setCardholderLName(e.target.value)} />
        
        <label>Email</label>
        <input type="text" value={email} onChange={(e) => setEmail(e.target.value)} />
        
        <label>Card Processor</label>
        <select value={processor} onChange={(e) => setProcessor(e.target.value)}>
          <option value="Visa">Visa</option>
          <option value="Mastercard">Mastercard</option>
          <option value="American Express">American Express</option>
          <option value="Discover">Discover</option>
        </select>
        
        <label>Card Number</label>
        <input type="text" value={cardNumber} onChange={(e) => setCardNumber(e.target.value)} />
        
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
          <div>
            <label>Expiration</label>
            <input type="text" placeholder="MM/YY" value={expiration} onChange={(e) => setExpiration(e.target.value)} style={{ width: '100%' }} />
          </div>
          <div>
            <label>CVC</label>
            <input type="text" value={cvc} onChange={(e) => setCvc(e.target.value)} style={{ width: '100%' }} />
          </div>
        </div>
        
        <label>Billing Address</label>
        <input type="text" value={address} onChange={(e) => setAddress(e.target.value)} />
        
        <label>Address Line 2</label>
        <input type="text" value={address2} onChange={(e) => setAddress2(e.target.value)} />
        
        <label>City</label>
        <input type="text" value={city} onChange={(e) => setCity(e.target.value)} />
        
        <label>State</label>
        <USStatesDropdown value={state} onChange={setState} />
        
        <label>Country/Province</label>
        <input type="text" value={country} onChange={(e) => setCountry(e.target.value)} />
        
        <label>Postal/Zip Code</label>
        <input type="text" value={zip} onChange={(e) => setZip(e.target.value)} />
        
        <SubmitCCInfoFormButton 
          cardholderFName={cardholderFName}
          cardholderLName={cardholderLName}
          processor={processor}
          cardNumber={parseInt(cardNumber)}
          expiration={expiration}
          cvc={parseInt(cvc)}
          address={address}
          address2={address2}
          city={city}
          state={state}
          country={country}
          zip={zip}
          customerId={parseInt(customerId)}
        />
      </form>
    </div>
  );
}