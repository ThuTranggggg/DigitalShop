# DigitalShop Microservices

Project demo he thong ban thiet bi cong nghe bang Django + Django REST Framework theo kien truc 4 microservice:

- `staff-service`
- `customer-service`
- `laptop-service`
- `mobile-service`
- `api-gateway` (Nginx)

Gateway hien phuc vu ca frontend va API. Mo `http://localhost:8000` de vao giao dien web.

## Cau truc thu muc

```text
microservices-shop/
├── staff-service/
├── customer-service/
├── laptop-service/
├── mobile-service/
├── api-gateway/
├── plantuml/
├── docs/
├── docker-compose.yml
├── .env.example
└── README.md
```

## Chay bang Docker

```bash
docker compose up --build
```

## Cau hinh database

- `staff-service`: MySQL
- `customer-service`: MySQL
- `laptop-service`: PostgreSQL
- `mobile-service`: PostgreSQL

Gateway:

- `http://localhost:8000`

Ports noi bo:

- `staff-service`: `8001`
- `customer-service`: `8002`
- `laptop-service`: `8003`
- `mobile-service`: `8004`

## Lenh migrate tung service

```bash
cd staff-service && python manage.py migrate
cd customer-service && python manage.py migrate
cd laptop-service && python manage.py migrate
cd mobile-service && python manage.py migrate
```

## Lenh seed data

```bash
cd staff-service && python manage.py seed_data
cd customer-service && python manage.py seed_data
cd laptop-service && python manage.py seed_data
cd mobile-service && python manage.py seed_data
```

## Tai khoan mau

- Staff: `admin / admin123`
- Customer 1: `customer01 / customer123`
- Customer 2: `customer02 / customer123`

## Endpoint chinh

### Staff

- `POST /api/staff/login/`
- `GET /api/staff/profile/`
- `POST /api/staff/laptops/`
- `PUT /api/staff/laptops/{id}/`
- `DELETE /api/staff/laptops/{id}/`
- `POST /api/staff/mobiles/`
- `PUT /api/staff/mobiles/{id}/`
- `DELETE /api/staff/mobiles/{id}/`
- `GET /api/staff/products/overview/`

### Customer

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

## Thu tu chup man hinh bao cao

1. Cau truc thu muc project.
2. Code model 4 service.
3. Code internal client staff/customer.
4. Nginx gateway config.
5. `docker-compose.yml`.
6. `makemigrations` va `migrate`.
7. `docker compose up --build`.
8. Staff login.
9. Staff them laptop/mobile.
10. Customer register/login.
11. Customer tim kiem san pham.
12. Customer tao gio hang va them san pham.
13. Customer cap nhat/xoa item.
14. Customer xem tong tien.
15. PlantUML sequence diagram.
