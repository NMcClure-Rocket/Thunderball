import ShippingAddressForm from "../components/forms/shipping-address-form";
import CCInfoForm from "../components/forms/cc-info-form";

export default function Checkout() {
  return (
    <div>
      <h1>Ayyyye I'm checkin' out 'ere!!!!</h1>
        <ShippingAddressForm />
        <CCInfoForm />
    </div>
  );
}
