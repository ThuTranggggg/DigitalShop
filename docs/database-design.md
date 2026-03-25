# Database Design

## staff-service (MySQL)

Table `staffs_staffuser`

- id
- full_name
- username
- email
- password
- role
- created_at
- updated_at

## customer-service (MySQL)

Table `customers_customeruser`

- id
- full_name
- username
- email
- phone
- password
- role
- created_at
- updated_at

Table `carts_cart`

- id
- customer_id
- created_at
- updated_at

Table `carts_cartitem`

- id
- cart_id
- product_type
- product_id
- product_name
- unit_price
- quantity
- subtotal

## laptop-service (PostgreSQL)

Table `laptops_laptop`

- id
- name
- brand
- cpu
- ram
- storage
- screen
- price
- stock
- description
- image_url
- created_at
- updated_at

## mobile-service (PostgreSQL)

Table `mobiles_mobile`

- id
- name
- brand
- chip
- ram
- storage
- battery
- camera
- price
- stock
- description
- image_url
- created_at
- updated_at
