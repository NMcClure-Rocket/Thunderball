---
description: Documentation for the Spellstack API endpoints, including request/response formats and example payloads.
---

# Spellstack API endpoints

The database tables for Spellstack are designed for quick API contract lookup. Use the endpoint index table to find routes by method and purpose, then use each endpoint's detail and field tables to validate required request inputs, response payloads, and expected status/error behavior during implementation and testing.

## Endpoint index

| Method | Endpoint | Purpose |
| --- | --- | --- |
| POST | `/logon` | Submit user credentials |
| GET | `/inventory` | Fetch all available items in the base price table |
| GET | `/inventory/{item_id}` | Fetches every variant by item ID |
| GET | `/pulse` | Health check / heartbeat endpoint |
| POST | `/purchase` | Submit a purchase order |
| POST | `/newcc` | Create a new credit card record |
| POST | `/newaddress` | Create a new shipping address record |
| POST | `/createuser` | Create a new user |
| GET | `/getcc/{id}` | Get credit cards for a given user |
| GET | `/getaddress/{id}` | Get shipping addresses for a given user |
| GET | `/orders/{id}` | Get all previous orders for a given user |

## POST /logon

Submit user credentials. This endpoint does not issue tokens and is not required for authentication in other endpoints, but it can be used to validate user credentials during login workflows.

**Details**  

| Category | Details |
| --- | --- |
| Method | `POST` |
| Path | `/logon` |
| Request body | `{"email": "jdoe", "pass": "mypassword"}` |
| Success response | `200 OK` -> `{"status": "ok", "customerid": 12}` |
| Error response | `401 Unauthorized` -> `{"status": "error", "customerid": null}` |

## GET /inventory

Fetch all available items in the base price table.

**Details**  

| Category | Details |
| --- | --- |
| Method | `GET` |
| Path | `/inventory` |
| Request body | None |
| Success response | `200 OK` -> `{"items": [{"id": 1, "name": "Duck Spell A", "price": 9.99, "image": "duck-a.png"}, {"id": 2, "name": "Duck Spell B", "price": 12.50, "image": "duck-b.png"}, {"id": 3, "name": "Fire Spell", "price": 5.00, "image": "fire.png"}]}` |
| Error responses | Not specified |

## GET /inventory/{item_id}

Fetcches all inventory for a given item ID.

**Details**  

| Category | Details |
| --- | --- |
| Method | `GET` |
| Path | `/inventory/{item_id}` |
| Path parameters | `item_id` (int), example: `GET /inventory/2` |
| Request body | None |
| Success response | `200 OK` -> `{"rows": [{"itemid": 1, "name": "Duck Spell A", "description": "...", "format": "Tome", "potency": 3, "reusable": "0", "category": "Conjuration", "price": 150.25, "amount": 7}, {"itemid": 2, "name": "Duck Spell A", "description": "...", "format": "PDF", "potency": 7, "reusable": "1", "category": "Conjuration", "price": 277.55, "amount": 3}]}` |
| Error response | `404 Not Found` -> `{"detail": "item not found"}` |

**Response fields**  

| Field | Type | Description |
| --- | --- | --- |
| `itemid` | int | Item ID |
| `name` | string | Name of the item |
| `description` | string | Description of the item |
| `format` | string | Format of the item (for example, Tome, PDF, Scroll) |
| `potency` | int | How strong the spell is |
| `reusable` | string or int | Reusable flag, either `0` or `1` |
| `category` | string | School/category of magic (for example, Illusion) |
| `price` | float | Price of the item |
| `amount` | int | Number of items available in stock |

## GET /pulse

Health check endpoint to verify API is running and responsive.

**Details**  

| Category | Details |
| --- | --- |
| Method | `GET` |
| Path | `/pulse` |
| Request body | None |
| Success response | `200 OK` -> `{"status": "ok", "timestamp": 1741868400000}` |
| Error responses | Not specified |

## POST /purchase

Submit a purchase order for an inventory item.

**Details**  

| Category | Details |
| --- | --- |
| Method | `POST` |
| Path | `/purchase` |
| Request body | `{"itemid": 1, "qty": 3, "transaction": 111.11, "customerid": 6, "addressid": 5, "ccid": 12}` |
| Success response | `200 OK` -> `{"status": "ok", "orderid": 1741868400000, "item": "Duck Spell A", "qty": 3, "total": 29.97}` |
| Error responses | `400 Bad Request` -> `{"detail": "Invalid request format"}`; `404 Not Found` -> `{"detail": "Item not found"}` |

**Request fields**  

| Field | Type | Description |
| --- | --- | --- |
| `itemid` | int | Item ID in the inventory database |
| `qty` | int | Number of items being purchased |
| `transaction` | float | Transaction price submitted with the purchase |
| `customerid` | int | Customer ID in the customer database |
| `addressid` | int | Address ID in the shipping address database |
| `ccid` | int | Credit card ID in the CCI table |

!!! note "note"
    The status code 200 (OK) is displayed whenever this endpoint called.

**Success response fields**  

| Field | Type | Description |
| --- | --- | --- |
| `status` | string | Always `ok` on success |
| `orderid` | int | Generated order ID (epoch milliseconds) |
| `item` | string | Purchased item name |
| `qty` | int | Quantity ordered |
| `total` | float | Calculated total (`price * qty`) |

## POST /newcc

Create a new credit card record in the database.

**Details**  

| Category | Details |
| --- | --- |
| Method | `POST` |
| Path | `/newcc` |
| Request body | `{"number": 11111111, "security_code": 111, "expiration": "12/12", "processor": "Visa", "first_name": "John", "last_name": "Doe", "address": "5555 Street Rd.", "addr_2": "Apt E111", "city": "Orlando", "state": "FL", "country": "United States", "zip": "11111", "customerid": 12}` |
| Success response | `200 OK` -> `{"status": "ok", "ccid": 12}` |
| Error response | `400 Bad Request` -> `{"detail": "Invalid request"}` |

**Request fields**  

| Field | Type | Description |
| --- | --- | --- |
| `number` | int | Credit card number |
| `security_code` | int | Three-digit security code |
| `expiration` | string | Expiration in `MM/YY` format |
| `processor` | string | Payment processor (for example, Visa, MasterCard) |
| `first_name` | string | Cardholder first name |
| `last_name` | string | Cardholder last name |
| `address` | string | Billing address line 1 |
| `addr_2` | string | Billing address line 2 |
| `city` | string | Billing city |
| `state` | string | Two-character state code (for example, AR) |
| `country` | string | Billing country |
| `zip` | string | Billing ZIP/postal code |
| `customerid` | int | Customer ID |

**Success response fields**  

| Field | Type | Description |
| --- | --- | --- |
| `status` | string | Always `ok` on success |
| `ccid` | int | ID of new or existing credit card in DB |

## POST /newaddress

Create a new shipping address record in the database.

**Details**  

| Category | Details |
| --- | --- |
| Method | `POST` |
| Path | `/newaddress` |
| Request body | `{"first_name": "John", "last_name": "Doe", "address": "5555 Street Rd.", "addr_2": "Apt E111", "city": "Orlando", "state": "FL", "country": "United States", "zip": "11111"}` |
| Success response | `200 OK` -> `{"status": "ok", "addressid": 12}` |
| Error response | `400 Bad Request` -> `{"detail": "Invalid request"}` |

**Request fields**  

| Field | Type | Description |
| --- | --- | --- |
| `first_name` | string | First name |
| `last_name` | string | Last name |
| `address` | string | Shipping address line 1 |
| `addr_2` | string | Shipping address line 2 |
| `city` | string | Shipping city |
| `state` | string | Two-character state code (for example, AR) |
| `country` | string | Shipping country |
| `zip` | string | Shipping ZIP/postal code |

**Success response fields**  

| Field | Type | Description |
| --- | --- | --- |
| `status` | string | Always `ok` on success |
| `addressid` | int | ID of new or existing address in DB |

## POST /createuser

Create a new user record.

**Details**  

| Category | Details |
| --- | --- |
| Method | `POST` |
| Path | `/createuser` |
| Request body | `{"first_name": "John", "last_name": "Doe", "user": "jdoe", "pass": "Password_123!"}` |
| Success response | `200 OK` -> `{"status": "ok"}` |
| Error response | `400 Bad Request` -> `{"detail": "Invalid request"}` |

**Request fields**  

| Field | Type | Description |
| --- | --- | --- |
| `first_name` | string | First name of new user |
| `last_name` | string | Last name of new user |
| `user` | string | Username of new user |
| `pass` | string | Password of new user |

**Success response fields**  

| Field | Type | Description |
| --- | --- | --- |
| `status` | string | Always `ok` on success |

## GET /getcc/{id}

Get the credit cards in the database for a given user.

**Details**  

| Category | Details |
| --- | --- |
| Method | `GET` |
| Path | `/getcc/{id}` |
| Path parameters | `id` (user/customer ID) |
| Request body | Generally none for GET. Existing docs may pass `{"customerID": 11}` |
| Success response | `200 OK` -> `{"rows": [{"number": 11111111, "security_code": 111, "expiration": "12/12", "processor": "Visa", "first_name": "John", "last_name": "Doe", "address": "5555 Street Rd.", "addr_2": "Apt E111", "city": "Orlando", "State": "FL", "country": "United States", "zip": "11111"}, {"number": 11111112, "security_code": 112, "expiration": "12/12", "processor": "Visa", "first_name": "John", "last_name": "Doe", "address": "5556 Street Blvd.", "addr_2": "Apt E121", "city": "Orlando", "State": "FL", "country": "United States", "zip": "11112"}]}` |
| Error response | `400 Bad Request` -> `{"detail": "Invalid request"}` |

**Response fields (rows[])**

| Field | Type | Description |
| --- | --- | --- |
| `number` | int | Credit card number |
| `security_code` | int | Three-digit security code |
| `expiration` | string | Expiration in `MM/YY` format |
| `processor` | string | Payment processor |
| `first_name` | string | Cardholder first name |
| `last_name` | string | Cardholder last name |
| `address` | string | Billing address line 1 |
| `addr_2` | string | Billing address line 2 |
| `city` | string | Billing city |
| `state` | string | Two-character state code |
| `country` | string | Billing country |
| `zip` | string | Billing ZIP/postal code |

## GET /getaddress/{id}

Get the shipping addresses in the database for a given user.

**Details**  

| Category | Details |
| --- | --- |
| Method | `GET` |
| Path | `/getaddress/{id}` |
| Path parameters | `id` (user/customer ID) |
| Request body | Generally none for GET. Existing docs may pass `{"customerID": 11}` |
| Success response | `200 OK` -> `{"rows": [{"first_name": "John", "last_name": "Doe", "address": "5555 Street Rd.", "addr_2": "Apt E111", "city": "Orlando", "State": "FL", "country": "United States", "zip": "11111"}, {"first_name": "John", "last_name": "Doe", "address": "5556 Street Blvd.", "addr_2": "Apt E121", "city": "Orlando", "State": "FL", "country": "United States", "zip": "11112"}]}` |
| Error response | `400 Bad Request` -> `{"detail": "Invalid request"}` |

**Response fields (rows[])**

| Field | Type | Description |
| --- | --- | --- |
| `first_name` | string | First name |
| `last_name` | string | Last name |
| `address` | string | Shipping address line 1 |
| `addr_2` | string | Shipping address line 2 |
| `city` | string | Shipping city |
| `state` | string | Two-character state code |
| `country` | string | Shipping country |
| `zip` | string | Shipping ZIP/postal code |

## GET /orders/{id}

Get all previous orders done by a given user.

**Details**  

| Category | Details |
| --- | --- |
| Method | `GET` |
| Path | `/orders/{id}` |
| Path parameters | `id` (user/customer ID) |
| Request body | Generally none for GET. Existing docs may pass `{"customerID": 11}` |
| Success response | `200 OK` -> `{"rows": [{"itemid": 1, "name": "Summon Rubber Ducky", "description": "...", "format": "Tome", "potency": 8, "reusable": "0", "category": "Invocation", "amount": 5, "transaction": 111.11, "purchase_time": "11/11/2010", "delivery_est": "11/11/2011", "imagelink": "..."}, {"itemid": 5, "name": "Hex of Fragmentation", "description": "...", "format": "PDF", "potency": 100, "reusable": "0", "category": "Curse", "amount": 1, "transaction": 150.25, "purchase_time": "12/01/2010", "delivery_est": "12/02/2010", "imagelink": "..."}]}` |
| Error responses | Not specified |

**Response fields (rows[])**

| Field | Type | Description |
| --- | --- | --- |
| `itemid` | int | Item ID in the inventory database |
| `name` | string | Name of the item |
| `description` | string | Description of the item |
| `format` | string | Format of the item (for example, Tome, PDF, Scroll) |
| `potency` | int | How strong the spell is |
| `reusable` | string or int | Reusable flag, either `0` or `1` |
| `category` | string | School of magic the spell belongs to |
| `amount` | int | Number of the item purchased |
| `transaction` | float | Total amount spent in the order |
| `purchase_time` | string | Purchase date in `MM/DD/YYYY` format |
| `delivery_est` | string | Estimated delivery date in `MM/DD/YYYY` format |
| `imagelink` | string | Link to the image representing the item |
