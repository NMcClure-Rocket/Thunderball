import SubmitFormButton from "../buttons/submit-form-button";
import USStatesDropdown from "../dropdowns/US-states-dropdown";

export default function CCInfoForm() {
  
  return (
    <div className="shipping-form-wrapper">
        <h1>Credit Card Checkout Form</h1>
      <form>
        <label>First Name</label>
        <input type="text"></input>
        <label>Last Name</label>
        <input type="text"></input>
        <label>Email</label>
        <input type="text"></input>
        <label>Card Number</label>
        <input type="text"></input>
        <label>Expiration</label>
        <input type="text" value="MM/YY"></input>
        <label>CVC</label>
        <input type="text"></input>
        <label>Billing Address</label>
        <input type="text"></input>
        <label>City</label>
        <input type="text"></input>
        <label>State</label>
        <USStatesDropdown />
        <label>Country/Province</label>
        <input type="text"></input>
        <label>Postal/Zip Code</label>
        <input type="text"></input>
        <SubmitFormButton />
      </form>
    </div>
  );
}