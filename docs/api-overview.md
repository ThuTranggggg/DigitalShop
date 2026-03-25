# API Overview

## Staff Service

- `POST /api/staff/login/`
- `GET /api/staff/profile/`
- `POST /api/staff/laptops/`
- `PUT /api/staff/laptops/{id}/`
- `DELETE /api/staff/laptops/{id}/`
- `POST /api/staff/mobiles/`
- `PUT /api/staff/mobiles/{id}/`
- `DELETE /api/staff/mobiles/{id}/`
- `GET /api/staff/products/overview/`

## Customer Service

- `POST /api/customers/register/`
- `POST /api/customers/login/`
- `GET /api/customers/profile/`
- `GET /api/customers/laptops/`
- `GET /api/customers/laptops/{id}/`
- `GET /api/customers/laptops/search/?q=&brand=&min_price=&max_price=`
- `GET /api/customers/mobiles/`
- `GET /api/customers/mobiles/{id}/`
- `GET /api/customers/mobiles/search/?q=&brand=&min_price=&max_price=`
- `POST /api/customers/cart/`
- `GET /api/customers/cart/`
- `POST /api/customers/cart/items/`
- `PUT /api/customers/cart/items/{id}/`
- `DELETE /api/customers/cart/items/{id}/`
- `GET /api/customers/cart/summary/`

## Direct Product Services

- `GET /api/laptops/`
- `GET /api/laptops/{id}/`
- `GET /api/laptops/search/?q=&brand=&min_price=&max_price=`
- `POST /api/laptops/`
- `PUT /api/laptops/{id}/`
- `DELETE /api/laptops/{id}/`
- `GET /api/mobiles/`
- `GET /api/mobiles/{id}/`
- `GET /api/mobiles/search/?q=&brand=&min_price=&max_price=`
- `POST /api/mobiles/`
- `PUT /api/mobiles/{id}/`
- `DELETE /api/mobiles/{id}/`
