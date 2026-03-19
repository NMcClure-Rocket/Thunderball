import SubmitShippingAddressFormButton from "../buttons/submit-shipping-address-form-button";
import USStatesDropdown from "../dropdowns/US-states-dropdown";
import { useState, useEffect } from "react";

export default function ShippingAddressForm() {
  const [fName, setfName] = useState('');
  const [lName, setlName] = useState('');
  const [address, setAddress] = useState('');
  const [address2, setAddress2] = useState('');
  const [city, setCity] = useState('');
  const [state, setState] = useState('');
  const [country, setCountry] = useState('');
  const [zip, setZip] = useState('');
  const [customerId, setCustomerId] = useState('');
  
     useEffect(() => {
        // Get customerId from localStorage on component mount
        const storedCustomerId = localStorage.getItem('customerid');
        if (storedCustomerId) {
          setCustomerId(storedCustomerId);
          console.log("Loaded customerid from localStorage:", storedCustomerId);
        }
      }, []);

  return (
    <div className="shipping-form-wrapper">
        <h1>Shipping Address Form</h1>
      <form>
        <label>First Name</label>
        <input type="text" value={fName} onChange={(e) => setfName(e.target.value)} />
        
        <label>Last Name</label>
        <input type="text" value={lName} onChange={(e) => setlName(e.target.value)} />
        
        <label>Shipping Address</label>
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
        
        <SubmitShippingAddressFormButton 
          fName={fName}
          lName={lName}
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