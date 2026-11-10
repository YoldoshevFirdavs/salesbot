# 🤖 SalesBot - Telegram E-Commerce Bot with Stripe Integration

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.0%2B-darkgreen?style=flat-square&logo=django)](https://www.djangoproject.com/)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-0088cc?style=flat-square&logo=telegram)](https://telegram.org/)
[![Stripe](https://img.shields.io/badge/Stripe-Payment-005EB8?style=flat-square&logo=stripe)](https://stripe.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13%2B-336791?style=flat-square&logo=postgresql)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

**A complete, production-ready Telegram bot for e-commerce with integrated payment processing, multi-language support, and beautiful UI.**

[Features](#-features) • [Tech Stack](#-tech-stack) • [Installation](#-installation) • [Usage](#-usage) • [Configuration](#-configuration) • [Contributing](#-contributing)

</div>

---

## ✨ Features

### 🤖 Telegram Bot
- **Interactive Menu System** - Browse products by category
- **Multi-Language Support** - Uzbek, Russian, English
- **Shopping Cart** - Add/remove items with quantity adjustment
- **Order Management** - View order history and status
- **Location Sharing** - Delivery address via GPS
- **Real-Time Notifications** - Order updates via Telegram

### 💳 Payment Processing
- **Stripe Integration** - Secure card payments
- **Multiple Payment Methods** - Cash on delivery & card payment
- **Order Confirmation** - Automatic payment success notifications
- **Webhook Support** - Real-time payment updates
- **Transaction Logging** - Complete payment history

### 📊 Admin Dashboard
- **Order Management** - View and manage orders
- **Product Management** - Add/edit products and images
- **Category Organization** - Hierarchical product categories
- **Sales Analytics** - Track revenue and orders
- **User Management** - View customer information

### 🎨 Modern UI
- **Glassmorphism Design** - Beautiful blur effects
- **Dark/Light Mode** - Theme switching
- **Responsive Layout** - Mobile-first design
- **Smooth Animations** - 60fps CSS animations
- **Gradient Buttons** - Modern button styling
- **Premium Checkout** - Beautiful payment page
- **Success Animations** - Celebratory confetti effects

### 🛠️ Technical Features
- **RESTful API** - Comprehensive API endpoints
- **JWT Authentication** - Secure token-based auth
- **Database Models** - Orders, Products, Categories, Users
- **Logging System** - Detailed application logs
- **Error Handling** - Comprehensive error management
- **Docker Support** - Containerized deployment

---

## 🏗️ Tech Stack

### Backend
- **Framework:** Django 4.0+
- **API:** Django REST Framework
- **Database:** PostgreSQL 13+
- **Cache:** Redis
- **Task Queue:** Celery (optional)

### Frontend
- **Language:** HTML5, CSS3, JavaScript (ES6+)
- **Design:** CSS Custom Properties, Gradients, Animations
- **Framework:** Vanilla JavaScript (no heavy dependencies)
- **Responsive:** Mobile-first design

### Telegram
- **Library:** python-telegram-bot
- **Handler:** Update/Message handlers
- **Storage:** User state management

### Payment
- **Provider:** Stripe
- **Method:** Checkout Sessions
- **Webhooks:** Event-driven payments

### Infrastructure
- **Container:** Docker & Docker Compose
- **Web Server:** Gunicorn + Nginx
- **OS:** Ubuntu/Debian

---

## 🚀 Installation

### Prerequisites
- Python 3.8+
- PostgreSQL 13+
- Docker & Docker Compose (optional)
- Telegram Bot Token (from @BotFather)
- Stripe API Keys

### Local Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/salesbot.git
cd salesbot
```

2. **Create virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your credentials
```

5. **Run migrations**
```bash
python manage.py migrate
```

6. **Create superuser**
```bash
python manage.py createsuperuser
```

7. **Collect static files**
```bash
python manage.py collectstatic --noinput
```

8. **Run development server**
```bash
python manage.py runserver
```

9. **Start Telegram bot** (in another terminal)
```bash
python tgbot/tgb/runbot.py
```

### Docker Setup

```bash
docker-compose up -d
```

This will start:
- Django web server (port 8000)
- PostgreSQL database
- Telegram bot
- Nginx reverse proxy (port 80)

---

## 📋 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Django
DEBUG=False
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com

# Database
DB_NAME=salestgbot
DB_USER=postgres
DB_PASSWORD=your-db-password
DB_HOST=db
DB_PORT=5432

# Telegram
BOT_TOKEN=your-telegram-bot-token
API_BASE_URL=http://127.0.0.1:8000

# Stripe
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Security
CSRF_COOKIE_SECURE=True
SESSION_COOKIE_SECURE=True
```

### Stripe Setup

1. Go to [Stripe Dashboard](https://dashboard.stripe.com)
2. Copy your API keys to `.env`
3. Set up webhook endpoint: `https://yourdomain.com/api/v1/payments/webhook/`
4. Subscribe to `checkout.session.completed` event

---

## 💻 Usage

### Telegram Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Start the bot and choose language |
| `/menu` | Browse product categories |
| `/cart` | View shopping cart |
| `/orders` | View your orders |
| `/help` | Get help |
| `/settings` | Change language/preferences |

### API Endpoints

#### Products
```
GET    /api/v1/products/           - List all products
GET    /api/v1/products/<id>/      - Get product details
POST   /api/v1/products/           - Create product (admin)
PUT    /api/v1/products/<id>/      - Update product (admin)
DELETE /api/v1/products/<id>/      - Delete product (admin)
```

#### Orders
```
GET    /api/v1/orders/             - List user orders
GET    /api/v1/orders/<id>/        - Get order details
POST   /api/v1/orders/             - Create order
PUT    /api/v1/orders/<id>/        - Update order (admin)
DELETE /api/v1/orders/<id>/        - Delete order (admin)
```

#### Payment
```
POST   /api/v1/payments/webhook/   - Stripe webhook endpoint
GET    /payment-success/<id>/      - Payment success page
GET    /checkout/<id>/             - Checkout page
```

---

## 📁 Project Structure

```
salesbot/
├── config/                 # Django configuration
│   ├── settings.py        # Main settings
│   ├── urls.py            # URL routing
│   ├── wsgi.py            # WSGI config
│   └── asgi.py            # ASGI config
├── tgbot/                  # Telegram bot app
│   ├── models.py          # Database models
│   ├── views.py           # API views
│   ├── urls.py            # Bot URL routing
│   ├── tgb/               # Bot implementation
│   │   ├── runbot.py      # Bot entry point
│   │   ├── inlines.py     # Inline handlers
│   │   ├── database.py    # Database queries
│   │   ├── messages.py    # Message handlers
│   │   ├── order_utils.py # Order utilities
│   │   └── logger.py      # Logging setup
│   └── data/              # Bot data
├── payment/                # Payment app
│   ├── models.py          # Payment models
│   ├── views.py           # Payment views
│   ├── urls.py            # Payment URLs
│   └── exceptions.py      # Custom exceptions
├── users/                  # User authentication
│   ├── models.py          # User model
│   ├── views.py           # Auth views
│   └── serializers.py     # Serializers
├── dashboard/             # Admin dashboard
│   ├── models.py          # Dashboard models
│   ├── views.py           # Dashboard views
│   └── urls.py            # Dashboard URLs
├── templates/             # HTML templates
│   ├── header.html        # Reusable header
│   ├── checkout.html      # Checkout page
│   ├── payment_success.html # Success page
│   └── theme.css          # Global styles
├── static/                # Static files
│   ├── images/            # Images
│   └── css/               # Additional CSS
├── media/                 # User uploads
│   └── products/          # Product images
├── logs/                  # Application logs
├── docker-compose.yml     # Docker setup
├── Dockerfile             # Docker image
├── requirements.txt       # Python dependencies
├── manage.py              # Django management
└── README.md              # This file
```

---

## 🔐 Security

- ✅ CSRF protection on forms
- ✅ JWT token authentication
- ✅ SQL injection prevention (ORM)
- ✅ XSS protection
- ✅ HTTPS enforced (production)
- ✅ Secure password hashing
- ✅ Rate limiting
- ✅ Input validation
- ✅ Secure webhook verification

---

## 🧪 Testing

### Run Tests
```bash
python manage.py test
```

### Test Coverage
```bash
coverage run --source='.' manage.py test
coverage report
```

### API Testing with cURL
```bash
# Get products
curl http://localhost:8000/api/v1/products/

# Create order
curl -X POST http://localhost:8000/api/v1/orders/ \
  -H "Content-Type: application/json" \
  -d '{"user": 1, "total_price": 50000}'
```

---

## 📊 Database Schema

### Users
```
- id (PK)
- chat_id (Telegram)
- phone_number
- language (uz/ru/eng)
- state
- created_at
- updated_at
```

### Products
```
- id (PK)
- name_uz, name_ru, name_eng
- description_uz, description_ru, description_eng
- price
- stock
- category (FK)
- image
- created_at
- updated_at
```

### Orders
```
- id (PK)
- user (FK)
- total_price
- status (Pending/Accepted/Completed/Cancelled)
- payment_method (cash/card)
- phone_number
- address
- created_at
- updated_at
```

### Payments
```
- id (PK)
- order (FK)
- stripe_payment_id
- amount
- currency
- status (pending/succeeded/failed)
- created_at
- updated_at
```

---

## 🐛 Troubleshooting

### Bot not responding
```bash
# Check if bot is running
ps aux | grep runbot.py

# Check logs
tail -f logs/telegram_bot.log

# Restart bot
python tgbot/tgb/runbot.py
```

### Database connection error
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Check credentials in .env
# Verify DB exists
psql -U postgres -l
```

### Stripe webhook not working
```
1. Verify webhook secret in .env
2. Check endpoint URL in Stripe Dashboard
3. View webhook logs in Stripe Dashboard
4. Test webhook: stripe trigger payment_intent.succeeded
```

### Static files not loading
```bash
python manage.py collectstatic --noinput
# Or in production:
python manage.py collectstatic --noinput --no-input
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit your changes** (`git commit -m 'Add AmazingFeature'`)
4. **Push to the branch** (`git push origin feature/AmazingFeature`)
5. **Open a Pull Request**

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for our code of conduct and development process.

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Firdavs** - *SalesBot Creator*
- GitHub: [@yourusername](https://github.com/yourusername)
- Telegram: [@yourhandle](https://t.me/yourhandle)
- Email: your.email@example.com

---

## 🙏 Acknowledgments

- [Django](https://www.djangoproject.com/) - Web framework
- [Telegram](https://telegram.org/) - Messaging platform
- [Stripe](https://stripe.com/) - Payment processing
- [PostgreSQL](https://www.postgresql.org/) - Database
- All [contributors](CONTRIBUTORS.md) who have helped

---

## 📞 Support

- 📖 **Documentation:** Check `/docs` folder
- 🐛 **Issues:** [GitHub Issues](https://github.com/yourusername/salesbot/issues)
- 💬 **Discussions:** [GitHub Discussions](https://github.com/yourusername/salesbot/discussions)
- 📧 **Email:** your.email@example.com

---

<div align="center">

Made with ❤️ by Firdavs

⭐ If you find this project helpful, please give it a star!

</div>
