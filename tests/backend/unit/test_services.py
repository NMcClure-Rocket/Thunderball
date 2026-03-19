"""
Unit tests for all API service modules.

Tests auth, inventory, purchase, address, and credit-card services in isolation
(no HTTP layer, no DB2 connection required).
"""
# pylint: disable=missing-class-docstring,missing-function-docstring
# pylint: disable=redefined-outer-name

import pytest


# ===========================================================================
# auth_service – authenticate
# ===========================================================================

class TestAuthenticate:
    def test_valid_credentials_return_true(self):
        from api.services.auth_service import authenticate
        assert authenticate("jdoe@a.com", "mypassword") is True

    def test_second_seeded_user_valid(self):
        from api.services.auth_service import authenticate
        assert authenticate("admin", "admin123") is True

    def test_wrong_password_returns_false(self):
        from api.services.auth_service import authenticate
        assert authenticate("jdoe@a.com", "wrongpass") is False

    def test_unknown_user_returns_false(self):
        from api.services.auth_service import authenticate
        assert authenticate("nobody@a.com", "mypassword") is False

    def test_empty_user_returns_false(self):
        from api.services.auth_service import authenticate
        assert authenticate("", "mypassword") is False

    def test_empty_password_returns_false(self):
        from api.services.auth_service import authenticate
        assert authenticate("jdoe@a.com", "") is False

    def test_both_empty_returns_false(self):
        from api.services.auth_service import authenticate
        assert authenticate("", "") is False

    def test_case_sensitive_password(self):
        from api.services.auth_service import authenticate
        assert authenticate("jdoe@a.com", "MyPassword") is False


# ===========================================================================
# auth_service – create_user
# ===========================================================================

class TestCreateUser:
    @pytest.fixture(autouse=True)
    def reset_users(self):
        """Restore _users to its original state after each test."""
        import api.services.auth_service as svc
        original = list(svc._users)
        yield
        svc._users[:] = original

    def test_new_user_returns_true(self):
        from api.services.auth_service import create_user
        assert create_user("New", "Person", "newperson@test.com", "pass") is True

    def test_duplicate_username_returns_false(self):
        from api.services.auth_service import create_user
        assert create_user("Dup", "User", "jdoe@a.com", "anything") is False

    def test_admin_duplicate_returns_false(self):
        from api.services.auth_service import create_user
        assert create_user("Admin", "Dup", "admin", "newpass") is False

    def test_created_user_can_then_authenticate(self):
        from api.services.auth_service import create_user, authenticate
        create_user("Alice", "Smith", "alice@test.com", "secret99")
        assert authenticate("alice@test.com", "secret99") is True

    def test_created_user_appears_in_list(self):
        import api.services.auth_service as svc
        svc.create_user("Bob", "Jones", "bob@test.com", "pw")
        assert any(u["email"] == "bob@test.com" for u in svc._users)

    def test_first_name_stored(self):
        import api.services.auth_service as svc
        svc.create_user("Carl", "Young", "carl@test.com", "pw")
        user = next(u for u in svc._users if u["email"] == "carl@test.com")
        assert user["first_name"] == "Carl"

    def test_last_name_stored(self):
        import api.services.auth_service as svc
        svc.create_user("Dana", "White", "dana@test.com", "pw")
        user = next(u for u in svc._users if u["email"] == "dana@test.com")
        assert user["last_name"] == "White"

    def test_second_create_for_same_user_still_false(self):
        from api.services.auth_service import create_user
        create_user("Eve", "Test", "eve@test.com", "pw")
        assert create_user("Eve", "Test", "eve@test.com", "different") is False


# ===========================================================================
# inventory_service – get_all_items
# ===========================================================================

class TestGetAllItems:
    def test_returns_list(self):
        from api.services.inventory_service import get_all_items
        assert isinstance(get_all_items(), list)

    def test_returns_at_least_one_item(self):
        from api.services.inventory_service import get_all_items
        assert len(get_all_items()) > 0

    def test_items_have_id_field(self):
        from api.services.inventory_service import get_all_items
        for item in get_all_items():
            assert "id" in item

    def test_items_have_name_field(self):
        from api.services.inventory_service import get_all_items
        for item in get_all_items():
            assert "name" in item

    def test_items_have_price_field(self):
        from api.services.inventory_service import get_all_items
        for item in get_all_items():
            assert "price" in item

    def test_items_have_image_field(self):
        from api.services.inventory_service import get_all_items
        for item in get_all_items():
            assert "image" in item

    def test_all_prices_are_positive(self):
        from api.services.inventory_service import get_all_items
        assert all(i["price"] > 0 for i in get_all_items())

    def test_returns_independent_copy(self):
        from api.services.inventory_service import get_all_items
        a = get_all_items()
        b = get_all_items()
        assert a is not b

    def test_seeded_items_1_2_present(self):
        from api.services.inventory_service import get_all_items
        ids = {i["id"] for i in get_all_items()}
        assert {1, 2}.issubset(ids)


# ===========================================================================
# inventory_service – get_item_by_id
# ===========================================================================

class TestGetItemById:
    def test_returns_item_for_id_1(self):
        from api.services.inventory_service import get_item_by_id
        item = get_item_by_id(1)
        assert item is not None
        assert item["base_info"] == 1

    def test_returns_item_for_id_2(self):
        from api.services.inventory_service import get_item_by_id
        item = get_item_by_id(2)
        assert item is not None
        assert item["base_info"] == 2

    def test_returns_none_for_id_3(self):
        from api.services.inventory_service import get_item_by_id
        assert get_item_by_id(3) is None

    def test_returns_none_for_unknown_id(self):
        from api.services.inventory_service import get_item_by_id
        assert get_item_by_id(9999) is None

    def test_returns_none_for_zero(self):
        from api.services.inventory_service import get_item_by_id
        assert get_item_by_id(0) is None

    def test_returned_item_has_all_required_fields(self):
        from api.services.inventory_service import get_item_by_id
        item = get_item_by_id(1)
        for field in ("itemID", "name", "description", "format", "potency",
                      "reusable", "category", "price", "amount", "base_info"):
            assert field in item

    def test_returned_item_price_is_positive(self):
        from api.services.inventory_service import get_item_by_id
        assert get_item_by_id(1)["price"] > 0


# ===========================================================================
# purchase_service – process_purchase
# ===========================================================================

class TestProcessPurchase:
    def test_returns_dict_for_valid_item(self):
        from api.services.purchase_service import process_purchase
        result = process_purchase(1, 2)
        assert isinstance(result, dict)

    def test_returns_none_for_unknown_item(self):
        from api.services.purchase_service import process_purchase
        assert process_purchase(9999, 1) is None

    def test_status_is_ok(self):
        from api.services.purchase_service import process_purchase
        assert process_purchase(1, 1)["status"] == "ok"

    def test_qty_matches_input(self):
        from api.services.purchase_service import process_purchase
        assert process_purchase(2, 5)["qty"] == 5

    def test_total_is_price_times_qty(self):
        from api.services.inventory_service import get_item_by_id
        from api.services.purchase_service import process_purchase
        item = get_item_by_id(1)
        result = process_purchase(1, 3)
        assert abs(result["total"] - item["price"] * 3) < 0.001

    def test_order_id_is_positive_integer(self):
        from api.services.purchase_service import process_purchase
        result = process_purchase(1, 1)
        assert isinstance(result["orderId"], int)
        assert result["orderId"] > 0

    def test_item_name_matches_inventory(self):
        from api.services.inventory_service import get_item_by_id
        from api.services.purchase_service import process_purchase
        item = get_item_by_id(2)
        result = process_purchase(2, 1)
        assert result["item"] == item["name"]

    def test_qty_1_total_equals_price(self):
        from api.services.inventory_service import get_item_by_id
        from api.services.purchase_service import process_purchase
        item = get_item_by_id(2)
        result = process_purchase(2, 1)
        assert abs(result["total"] - item["price"]) < 0.001

    def test_all_required_keys_present(self):
        from api.services.purchase_service import process_purchase
        result = process_purchase(1, 1)
        for key in ("status", "orderId", "item", "qty", "total"):
            assert key in result


# ===========================================================================
# address_service – get_addresses_by_customer
# ===========================================================================

class TestGetAddressesByCustomer:
    @pytest.fixture(autouse=True)
    def reset_addresses(self):
        import api.services.address_service as svc
        original = list(svc._addresses)
        original_next = svc._next_id
        yield
        svc._addresses[:] = original
        svc._next_id = original_next

    def test_returns_list(self):
        from api.services.address_service import get_addresses_by_customer
        assert isinstance(get_addresses_by_customer(1), list)

    def test_returns_addresses_for_seeded_customer(self):
        from api.services.address_service import get_addresses_by_customer
        assert len(get_addresses_by_customer(1)) >= 1

    def test_returns_empty_for_unknown_customer(self):
        from api.services.address_service import get_addresses_by_customer
        assert get_addresses_by_customer(9999) == []

    def test_id_not_in_result(self):
        from api.services.address_service import get_addresses_by_customer
        for addr in get_addresses_by_customer(1):
            assert "id" not in addr

    def test_customer_id_not_in_result(self):
        from api.services.address_service import get_addresses_by_customer
        for addr in get_addresses_by_customer(1):
            assert "customer_id" not in addr

    def test_address_fields_present(self):
        from api.services.address_service import get_addresses_by_customer
        for addr in get_addresses_by_customer(1):
            assert "address" in addr
            assert "city" in addr
            assert "state" in addr
            assert "zip" in addr


# ===========================================================================
# address_service – create_address
# ===========================================================================

class TestCreateAddress:
    @pytest.fixture(autouse=True)
    def reset_addresses(self):
        import api.services.address_service as svc
        original = list(svc._addresses)
        original_next = svc._next_id
        yield
        svc._addresses[:] = original
        svc._next_id = original_next

    def _sample(self):
        return {
            "first_name": "Jane", "last_name": "Doe",
            "address": "1 Main St", "addr_2": "",
            "city": "Miami", "state": "FL", "country": "US", "zip": "33101",
        }

    def test_creates_address_in_store(self):
        import api.services.address_service as svc
        before = len(svc._addresses)
        svc.create_address(2, self._sample())
        assert len(svc._addresses) == before + 1

    def test_increments_next_id(self):
        import api.services.address_service as svc
        before = svc._next_id
        svc.create_address(2, self._sample())
        assert svc._next_id == before + 1

    def test_created_address_retrievable_by_customer(self):
        from api.services.address_service import create_address, get_addresses_by_customer
        create_address(42, {**self._sample(), "city": "Tampa"})
        result = get_addresses_by_customer(42)
        assert len(result) == 1
        assert result[0]["city"] == "Tampa"

    def test_multiple_creates_for_same_customer(self):
        from api.services.address_service import create_address, get_addresses_by_customer
        create_address(55, {**self._sample(), "city": "A"})
        create_address(55, {**self._sample(), "city": "B"})
        assert len(get_addresses_by_customer(55)) == 2

    def test_customer_id_stored_correctly(self):
        import api.services.address_service as svc
        svc.create_address(77, self._sample())
        created = [a for a in svc._addresses if a["customer_id"] == 77]
        assert len(created) == 1


# ===========================================================================
# credit_card_service – get_cards_by_customer
# ===========================================================================

class TestGetCardsByCustomer:
    @pytest.fixture(autouse=True)
    def reset_cards(self):
        import api.services.credit_card_service as svc
        original = list(svc._credit_cards)
        original_next = svc._next_id
        yield
        svc._credit_cards[:] = original
        svc._next_id = original_next

    def test_returns_list(self):
        from api.services.credit_card_service import get_cards_by_customer
        assert isinstance(get_cards_by_customer(1), list)

    def test_returns_cards_for_seeded_customer(self):
        from api.services.credit_card_service import get_cards_by_customer
        assert len(get_cards_by_customer(1)) >= 1

    def test_returns_empty_for_unknown_customer(self):
        from api.services.credit_card_service import get_cards_by_customer
        assert get_cards_by_customer(9999) == []

    def test_id_not_in_result(self):
        from api.services.credit_card_service import get_cards_by_customer
        for card in get_cards_by_customer(1):
            assert "id" not in card

    def test_customer_id_not_in_result(self):
        from api.services.credit_card_service import get_cards_by_customer
        for card in get_cards_by_customer(1):
            assert "customer_id" not in card

    def test_card_fields_present(self):
        from api.services.credit_card_service import get_cards_by_customer
        for card in get_cards_by_customer(1):
            assert "number" in card
            assert "processor" in card
            assert "expiration" in card


# ===========================================================================
# credit_card_service – create_card
# ===========================================================================

class TestCreateCard:
    @pytest.fixture(autouse=True)
    def reset_cards(self):
        import api.services.credit_card_service as svc
        original = list(svc._credit_cards)
        original_next = svc._next_id
        yield
        svc._credit_cards[:] = original
        svc._next_id = original_next

    def _sample(self):
        return {
            "number": 4111111111111111, "security_code": 123,
            "expiration": "01/29", "processor": "Visa",
            "first_name": "Test", "last_name": "User",
            "address": "1 St", "addr_2": "", "city": "NYC",
            "state": "NY", "country": "US", "zip": "10001",
        }

    def test_creates_card_in_store(self):
        import api.services.credit_card_service as svc
        before = len(svc._credit_cards)
        svc.create_card(2, self._sample())
        assert len(svc._credit_cards) == before + 1

    def test_increments_next_id(self):
        import api.services.credit_card_service as svc
        before = svc._next_id
        svc.create_card(2, self._sample())
        assert svc._next_id == before + 1

    def test_created_card_retrievable_by_customer(self):
        from api.services.credit_card_service import create_card, get_cards_by_customer
        create_card(99, {**self._sample(), "processor": "Mastercard"})
        result = get_cards_by_customer(99)
        assert len(result) == 1
        assert result[0]["processor"] == "Mastercard"

    def test_customer_id_stored_correctly(self):
        import api.services.credit_card_service as svc
        svc.create_card(88, self._sample())
        created = [c for c in svc._credit_cards if c["customer_id"] == 88]
        assert len(created) == 1

    def test_multiple_cards_for_same_customer(self):
        from api.services.credit_card_service import create_card, get_cards_by_customer
        create_card(66, {**self._sample(), "processor": "Visa"})
        create_card(66, {**self._sample(), "processor": "Amex"})
        assert len(get_cards_by_customer(66)) == 2
