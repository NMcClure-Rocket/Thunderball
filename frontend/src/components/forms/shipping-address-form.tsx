import SubmitFormButton from "../buttons/submit-form-button";
import USStatesDropdown from "../dropdowns/US-states-dropdown";

export default function ShippingAddressForm() {
  
  return (
    <div className="shipping-form-wrapper">
        <h1>Shipping Address Form</h1>
      <form>
        <label>First Name</label>
        <input type="text"></input>
        <label>Last Name</label>
        <input type="text"></input>
        <label>Street Address</label>
        <input type="text"></input>
        <label>Address 2</label>
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