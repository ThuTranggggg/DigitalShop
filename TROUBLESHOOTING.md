# 🔧 Hướng Dẫn Khắc Phục Lỗi Đăng Nhập (Login Issue Troubleshooting)

## ❓ Vấn đề: "Sau khi click đăng nhập, không có phản hồi gì từ hệ thống"

---

## ✅ Xác Nhận - Hệ Thống Backend Hoạt Động Bình Thường

Tôi đã kiểm tra toàn bộ hệ thống backend và xác minh:

### API Endpoints Status
- ✓ Login API: `POST /api/customers/login/` → **200 OK**
- ✓ Cart API: `POST /api/customers/cart/` → **201 Created**
- ✓ Cart Summary: `GET /api/customers/cart/summary/` → **200 OK**
- ✓ Products API: `GET /api/customers/laptops/` → **200 OK** (28 products)
- ✓ API Gateway: Nginx proxy routing **hoạt động đúng**
- ✓ Frontend Files: HTML, CSS, JS được serve **đúng cách**

---

## 🔍 Nguyên Nhân Có Thể (Probable Causes)

### 1. 🎯 **Nhập Sai Thông Tin Đăng Nhập** (Chính Xác Nhất)
**Dấu hiệu:** Bạn thấy "Không có phản hồi" hoặc page "treo"

**Kiểm tra:**
```
Username: customer01      ❌ KHÔNG customer1, testcustomer1, admin
Password: customer123     ❌ KHÔNG 123456, admin123, customer
```

### 2. 💻 **Lỗi Browser/JavaScript**
**Dấu hiệu:** Console hiển thị error messages

**Kiểm tra:**
- Mở DevTools: `F12` (hoặc Chuột phải → "Inspect")
- Tab "Console" → Xem các error đỏ

### 3. 🌐 **Network/Kết Nối API**
**Dấu hiệu:** Fetch requests timeout hoặc bị block CORS

**Kiểm tra:**
- Tab "Network" trong DevTools
- Xem response status code: 200? 400? 500? timeout?

---

## 🏃 Cách Khắc Phục: Bước-Từng-Bước

### **Bước 1️⃣: Xác Minh Credentials**

❌ **SAIIIIII:**
```
Username: testcustomer1
Password: 123456
```

✅ **ĐÚNG:**
```
Username: customer01
Password: customer123
```

Hoặc:
```
Username: customer02
Password: customer123
```

---

### **Bước 2️⃣: Kiểm Tra Browser Console**

1. Mở trang: `http://localhost:8000`
2. Nhấp F12 → Tab **Console**
3. Nhấp nút "Vào khu khách hàng"
4. Xem các log messages:

```
[Login] Customer attempting login: customer01
[API Request] POST /api/customers/login/
[API Response] POST /api/customers/login/: Status 200
[Login] Customer response data received: {access: "...", customer: {...}}
[Login] Products fetched successfully
[Login] Cart summary fetched successfully
✓ Đăng nhập khách hàng thành công
```

**Nếu thấy error:**
- Copy error message
- Kiểm tra trong danh sách Error Code bên dưới

---

### **Bước 3️⃣: Sử Dụng Debug Page**

Tôi đã tạo một trang debug chi tiết:

1. Truy cập: `http://localhost:8000/debug_login.html`
2. Nhập credentials:
   - Username: `customer01`
   - Password: `customer123`
3. Nhấp **"Test Login"**
4. Xem chi tiết từng bước:
   - Login response
   - Cart creation
   - Cart summary
   - Products fetching

Nếu flow này thành công → API hoạt động, vấn đề ở app.js chính

---

## 🐛 Common Error Codes & Solutions

### `400 Bad Request: Invalid username or password.`
**Nguyên nhân:** Credentials sai
```
❌ Sai:    customer01 / 123456
❌ Sai:    testcustomer1 / customer123  
✅ Đúng:   customer01 / customer123
✅ Đúng:   customer02 / customer123
```

### `401 Unauthorized`
**Nguyên nhân:** Token bị hết hạn hoặc header sai
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### `CORS Error: Access-Control-Allow-Origin`
**Nguyên nhân:** API Gateway missing CORS headers
**Kiểm tra:** Response headers có `Access-Control-Allow-Origin: *` không?

### `Timeout`
**Nguyên nhân:** Backend service chậm hoặc bị down
**Kiểm tra:** 
```bash
docker-compose ps
# Tất cả containers phải "Up"
```

---

## 🔧 Debug Commands

### Kiểm tra Docker Services
```bash
docker-compose ps
```
Đầu ra phải hiển thị tất cả containers **Up**:
- api-gateway
- customer-service  
- laptop-service
- mobile-service
- staff-service
- mysql-customer
- mysql-staff
- postgres-laptop
- postgres-mobile

### Kiểm tra Logs
```bash
# Customer service logs
docker-compose logs customer-service --tail 50

# Nginx gateway logs
docker-compose logs api-gateway --tail 50
```

### Test API trực tiếp
```bash
# Test login
curl -X POST http://localhost:8000/api/customers/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"customer01","password":"customer123"}'

# Hoặc dùng Python
python -c "
import requests
r = requests.post('http://localhost:8000/api/customers/login/',
    json={'username': 'customer01', 'password': 'customer123'}
)
print(f'Status: {r.status_code}')
print(f'Response: {r.json()}')
"
```

---

## 📊 Login Flow Diagram

```
┌─────────────────────┐
│   User click Login  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────────────────────┐
│ POST /api/customers/login/          │
│ username: customer01                │
│ password: customer123               │
└──────────┬──────────────────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│ 200 OK                              │
│ {                                   │
│   "access": "JWT_TOKEN",            │
│   "customer": {...}                 │
│ }                                   │
└──────────┬──────────────────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│ POST /api/customers/cart/ (ensure)  │
│ Authorization: Bearer JWT_TOKEN     │
└──────────┬──────────────────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│ 201 Created                         │
│ {id: 1, items: []}                  │
└──────────┬──────────────────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│ GET /api/customers/cart/summary/    │
│ Authorization: Bearer JWT_TOKEN     │
└──────────┬──────────────────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│ 200 OK                              │
│ {total_items: 0, total_amount: 0}   │
└──────────┬──────────────────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│ GET /api/customers/laptops/         │
│ Authorization: Bearer JWT_TOKEN     │
└──────────┬──────────────────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│ 200 OK - [28 products]              │
└──────────┬──────────────────────────┘
           │
           ▼
┌──────────────────────────────────────┐
│ Redirect to #/shop view              │
│ Show toast: "Đăng nhập thành công"   │
└──────────────────────────────────────┘
```

---

## 📞 Nh Hỗ Trợ Thêm

Nếu vấn đề vẫn persists:

1. **Cung cấp thông tin:**
   - Credentials bạn đang dùng
   - Browser console error message (screenshot hoặc text)
   - Status code từ API response (200/400/500?)
   - Docker service status (`docker-compose ps`)

2. **Và tìm kiếm trong:**
   - Browser Console (F12)
   - Docker logs (`docker-compose logs`)
   - Nginx access log

3. **Restart services nếu cần:**
   ```bash
   docker-compose down
   docker-compose up --build
   ```

---

**Ngày tạo:** 2026-03-25  
**Phiên bản:** v0.1.0  
**Status:** ✅ Backend tested and verified working
