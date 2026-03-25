# Architecture Overview

DigitalShop duoc thiet ke theo kien truc microservice gom 4 service chinh:

- `staff-service`: xac thuc staff va proxy cac thao tac CRUD san pham.
- `customer-service`: dang ky, dang nhap customer, xem san pham va quan ly gio hang.
- `laptop-service`: luu tru va cung cap du lieu laptop.
- `mobile-service`: luu tru va cung cap du lieu mobile.

## Data Ownership

- `staff-service` su dung MySQL rieng cho tai khoan staff.
- `customer-service` su dung MySQL rieng cho tai khoan customer va cart.
- `laptop-service` su dung PostgreSQL rieng cho san pham laptop.
- `mobile-service` su dung PostgreSQL rieng cho san pham mobile.

## Service Communication

- Staff CRUD laptop/mobile thong qua `staff-service` -> HTTP REST -> product services.
- Customer xem/search san pham va kiem tra ton kho thong qua `customer-service` -> HTTP REST -> product services.
- API Gateway Nginx dung truoc toan bo he thong va route request theo prefix `/api/...`.

## Runtime Flow

1. Client goi API vao `api-gateway`.
2. Gateway route den service phu hop.
3. Service xu ly auth/business logic.
4. Neu can, service goi sang service khac qua REST.
5. Moi service chi thao tac database cua chinh no.
