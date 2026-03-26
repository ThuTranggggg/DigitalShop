# Sequence Diagram Overview

File PlantUML tong hop:

- `plantuml/digitalshop-sequence-diagrams.puml`

Bo sequence diagram nay mo ta cac luong chinh cua he thong hien tai:

1. Staff login
2. Staff dashboard load
3. Staff create product
4. Staff update product
5. Staff delete product
6. Staff import stock
7. Customer login
8. Customer browse product catalog
9. Customer create/get active cart
10. Customer add item to cart
11. Customer update cart item
12. Customer delete cart item
13. Customer checkout
14. Customer invoice history
15. Customer cancel pending invoice

Nhan to xuat hien trong sequence:

- `API Gateway`
- `staff-service`
- `customer-service`
- `cart-service`
- `laptop-service`
- `clothes-service`
- `MySQL Staff DB`
- `MySQL Customer DB`
- `PostgreSQL Cart DB`
- `PostgreSQL Laptop DB`
- `PostgreSQL Clothes DB`

Neu can render bang PlantUML CLI:

```bash
plantuml plantuml/digitalshop-sequence-diagrams.puml
```

Neu muon tach thanh tung file PNG/SVG de dua vao bao cao, co the giu nguyen file tong hop nay vi no da gom nhieu block `@startuml ... @enduml`.
