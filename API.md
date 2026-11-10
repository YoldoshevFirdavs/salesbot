# 📡 API Documentation

Complete API reference for SalesBot REST endpoints.

**Base URL:** `http://localhost:8000/api/v1`  
**Authentication:** JWT Token (Bearer token)

---

## 🔐 Authentication

### Get Token

**Request:**
```http
POST /token/
Content-Type: application/json

{
  "username": "admin",
  "password": "your_password"
}
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Using Token

Include in request header:
```http
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

### Refresh Token

**Request:**
```http
POST /token/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

---

## 🛍️ Products API

### List Products

**Request:**
```http
GET /products/?category=1&page=1
```

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `category` | integer | Filter by category ID |
| `page` | integer | Page number (default: 1) |
| `search` | string | Search by name |

**Response (200):**
```json
{
  "count": 50,
  "next": "http://localhost:8000/api/v1/products/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name_uz": "Пицца",
      "name_ru": "Пицца",
      "name_eng": "Pizza",
      "price": 50000,
      "stock": 10,
      "category": 1,
      "image": "http://localhost:8000/media/products/pizza.jpg",
      "created_at": "2024-11-10T10:00:00Z"
    }
  ]
}
```

### Get Product Detail

**Request:**
```http
GET /products/1/
```

**Response (200):**
```json
{
  "id": 1,
  "name_uz": "Пицца",
  "name_ru": "Пицца",
  "name_eng": "Pizza",
  "description_uz": "Вкусная пицца",
  "description_ru": "Вкусная пицца",
  "description_eng": "Delicious pizza",
  "price": 50000,
  "stock": 10,
  "category": 1,
  "image": "http://localhost:8000/media/products/pizza.jpg",
  "created_at": "2024-11-10T10:00:00Z",
  "updated_at": "2024-11-10T10:00:00Z"
}
```

### Create Product (Admin)

**Request:**
```http
POST /products/
Content-Type: application/json
Authorization: Bearer <token>

{
  "name_uz": "Пицца",
  "name_ru": "Пицца",
  "name_eng": "Pizza",
  "description_uz": "Вкусная пицца",
  "description_ru": "Вкусная пицца",
  "description_eng": "Delicious pizza",
  "price": 50000,
  "stock": 10,
  "category": 1
}
```

**Response (201):**
```json
{
  "id": 1,
  "name_uz": "Пицца",
  "price": 50000,
  ...
}
```

### Update Product (Admin)

**Request:**
```http
PUT /products/1/
Content-Type: application/json
Authorization: Bearer <token>

{
  "name_uz": "Пицца обновленная",
  "price": 55000
}
```

**Response (200):** Updated product object

### Delete Product (Admin)

**Request:**
```http
DELETE /products/1/
Authorization: Bearer <token>
```

**Response (204):** No content

---

## 🏪 Categories API

### List Categories

**Request:**
```http
GET /categories/?parent=null
```

**Response (200):**
```json
{
  "count": 5,
  "results": [
    {
      "id": 1,
      "name_uz": "Пиццы",
      "name_ru": "Пиццы",
      "name_eng": "Pizzas",
      "parent": null,
      "created_at": "2024-11-10T10:00:00Z"
    }
  ]
}
```

### Get Category Detail

**Request:**
```http
GET /categories/1/
```

**Response (200):** Category object with products

### Create Category (Admin)

**Request:**
```http
POST /categories/
Content-Type: application/json
Authorization: Bearer <token>

{
  "name_uz": "Салаты",
  "name_ru": "Салаты",
  "name_eng": "Salads",
  "parent": null
}
```

---

## 📦 Orders API

### List Orders

**Request:**
```http
GET /orders/?status=Pending&page=1
Authorization: Bearer <token>
```

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `status` | string | Filter: Pending/Accepted/Completed/Cancelled |
| `page` | integer | Page number |
| `user` | integer | Filter by user ID (admin only) |

**Response (200):**
```json
{
  "count": 10,
  "results": [
    {
      "id": 1,
      "user": {
        "id": 1,
        "full_name": "John Doe",
        "phone_number": "+998901234567"
      },
      "total_price": 150000,
      "status": "Pending",
      "payment_method": "card",
      "phone_number": "+998901234567",
      "address": "123 Main St",
      "created_at": "2024-11-10T10:00:00Z",
      "updated_at": "2024-11-10T10:00:00Z"
    }
  ]
}
```

### Get Order Detail

**Request:**
```http
GET /orders/1/
Authorization: Bearer <token>
```

**Response (200):** Order object with details

### Create Order

**Request:**
```http
POST /orders/
Content-Type: application/json
Authorization: Bearer <token>

{
  "user": 1,
  "items": [
    {
      "product": 1,
      "quantity": 2
    }
  ],
  "payment_method": "card",
  "phone_number": "+998901234567",
  "address": "123 Main St"
}
```

**Response (201):**
```json
{
  "id": 1,
  "user": 1,
  "total_price": 150000,
  "status": "Pending",
  ...
}
```

### Update Order (Admin)

**Request:**
```http
PUT /orders/1/
Content-Type: application/json
Authorization: Bearer <token>

{
  "status": "Accepted",
  "address": "New address"
}
```

**Response (200):** Updated order object

### Delete Order (Admin)

**Request:**
```http
DELETE /orders/1/
Authorization: Bearer <token>
```

**Response (204):** No content

---

## 💳 Payment API

### Create Payment Session

**Request:**
```http
POST /payments/create-session/
Content-Type: application/json

{
  "order_id": 1
}
```

**Response (200):**
```json
{
  "session_id": "cs_test_...",
  "checkout_url": "https://checkout.stripe.com/pay/..."
}
```

### Webhook Endpoint

**Request:**
```http
POST /payments/webhook/
Content-Type: application/json

{
  "id": "evt_...",
  "type": "checkout.session.completed",
  "data": {
    "object": {
      "id": "cs_test_...",
      "metadata": {
        "order_id": "1"
      }
    }
  }
}
```

**Response (200):**
```json
{
  "status": "ok"
}
```

---

## 👤 Users API

### Get Current User

**Request:**
```http
GET /users/me/
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@example.com",
  "full_name": "Admin User",
  "phone_number": "+998901234567",
  "language": "uz",
  "created_at": "2024-11-10T10:00:00Z"
}
```

### Update User Profile

**Request:**
```http
PUT /users/me/
Content-Type: application/json
Authorization: Bearer <token>

{
  "full_name": "New Name",
  "phone_number": "+998909876543",
  "language": "ru"
}
```

**Response (200):** Updated user object

### List Users (Admin)

**Request:**
```http
GET /users/?page=1
Authorization: Bearer <token>
```

**Response (200):** Paginated users list

---

## 🔍 Error Responses

### 400 Bad Request
```json
{
  "error": "Invalid request data",
  "details": {
    "field_name": ["Error message"]
  }
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

### 500 Server Error
```json
{
  "detail": "Internal server error"
}
```

---

## 📊 Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK |
| 201 | Created |
| 204 | No Content |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 500 | Server Error |

---

## 🧪 Testing with cURL

### Get Token
```bash
curl -X POST http://localhost:8000/api/v1/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "password"}'
```

### List Products
```bash
curl http://localhost:8000/api/v1/products/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Create Order
```bash
curl -X POST http://localhost:8000/api/v1/orders/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "user": 1,
    "total_price": 50000,
    "payment_method": "card",
    "phone_number": "+998901234567"
  }'
```

---

## 🔗 Rate Limiting

All endpoints have rate limits:
- **Authenticated:** 1000 requests/hour
- **Unauthenticated:** 100 requests/hour

Rate limit headers:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1699592400
```

---

## 📚 API Versioning

Current version: **v1**

API URL format: `/api/v1/endpoint`

Future versions will use: `/api/v2/endpoint`

---

## 🔐 Security

- All endpoints require HTTPS in production
- JWT tokens expire after 1 hour
- Refresh tokens expire after 7 days
- All data is validated
- SQL injection protection
- XSS protection enabled
- CORS properly configured

---

## 💬 Support

- 📖 [Full Documentation](README.md)
- 🐛 [Report Issue](https://github.com/yourusername/salesbot/issues)
- 💬 [Discussions](https://github.com/yourusername/salesbot/discussions)

---

<div align="center">

**Last Updated:** November 10, 2024

🚀 Ready to integrate? Start with [Installation](INSTALLATION.md)

</div>
