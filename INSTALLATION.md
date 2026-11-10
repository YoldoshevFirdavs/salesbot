# 🚀 Installation & Setup Guide

Complete guide to install and set up SalesBot on your local machine or server.

---

## 📋 Requirements

### System Requirements
- **OS:** Ubuntu 20.04+, Debian 10+, or Windows 10+
- **RAM:** 2GB minimum, 4GB recommended
- **Disk:** 10GB free space
- **CPU:** 2 cores minimum

### Software Requirements
- **Python:** 3.8+ ([Download](https://www.python.org/downloads/))
- **PostgreSQL:** 13+ ([Download](https://www.postgresql.org/download/))
- **Git:** Latest version ([Download](https://git-scm.com/))
- **Docker:** Optional, for containerized setup ([Download](https://www.docker.com/))

---

## 🔧 Local Development Setup

### Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/salesbot.git
cd salesbot
```

### Step 2: Create Virtual Environment

**On Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt  # For development
```

### Step 4: Install PostgreSQL

**On Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

**On macOS:**
```bash
brew install postgresql@14
brew services start postgresql@14
```

**On Windows:**
- Download installer from [postgresql.org](https://www.postgresql.org/download/windows/)
- Run installer with default options
- Remember the password you set!

### Step 5: Create Database

```bash
# Open PostgreSQL terminal
psql -U postgres

# Create database and user
CREATE DATABASE salestgbot;
CREATE USER salesbot_user WITH PASSWORD 'your_secure_password';

ALTER ROLE salesbot_user SET client_encoding TO 'utf8';
ALTER ROLE salesbot_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE salesbot_user SET default_transaction_deferrable TO on;
ALTER ROLE salesbot_user SET timezone TO 'UTC';

GRANT ALL PRIVILEGES ON DATABASE salestgbot TO salesbot_user;

# Exit
\q
```

### Step 6: Configure Environment

Create `.env` file in project root:

```bash
cp .env.example .env
```

Edit `.env`:

```env
# Django
DEBUG=True
DJANGO_SECRET_KEY=your-secret-key-generate-one-here
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=salestgbot
DB_USER=salesbot_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432

# Telegram
BOT_TOKEN=123456789:ABCDefGHIjklMNOpqrsTUVwxyz
API_BASE_URL=http://127.0.0.1:8000

# Stripe (Get from https://dashboard.stripe.com/)
STRIPE_PUBLISHABLE_KEY=pk_test_your_key_here
STRIPE_SECRET_KEY=sk_test_your_key_here
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret

# Security
CSRF_COOKIE_SECURE=False  # True in production
SESSION_COOKIE_SECURE=False  # True in production
```

### Step 7: Run Migrations

```bash
python manage.py migrate
```

### Step 8: Create Superuser

```bash
python manage.py createsuperuser
```

Follow prompts to create admin user.

### Step 9: Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### Step 10: Start Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser.

### Step 11: Start Telegram Bot

In a new terminal (with venv activated):

```bash
python tgbot/tgb/runbot.py
```

---

## 🐳 Docker Setup

### Step 1: Install Docker

- **Windows/macOS:** [Docker Desktop](https://www.docker.com/products/docker-desktop)
- **Linux:** 
  ```bash
  sudo apt-get install docker.io docker-compose
  ```

### Step 2: Configure Environment

```bash
cp .env.example .env
```

Edit `.env` for Docker:

```env
# Database (use 'db' as host in Docker)
DB_HOST=db
DB_PORT=5432

# Use container names instead of localhost
API_BASE_URL=http://web:8000
```

### Step 3: Build and Start

```bash
docker-compose build
docker-compose up -d
```

Check logs:
```bash
docker-compose logs -f
```

### Step 4: Run Migrations

```bash
docker-compose exec web python manage.py migrate
```

### Step 5: Create Superuser

```bash
docker-compose exec web python manage.py createsuperuser
```

### Step 6: Access Application

- **Web:** http://localhost
- **Admin:** http://localhost/admin
- **API:** http://localhost/api/v1/

---

## ⚙️ Configuration Details

### Telegram Bot Token

1. Open Telegram
2. Search for [@BotFather](https://t.me/botfather)
3. Send `/newbot`
4. Follow instructions
5. Copy token to `.env`

### Stripe Setup

1. Go to [Stripe Dashboard](https://dashboard.stripe.com)
2. Sign up or log in
3. Go to Developers → API Keys
4. Copy:
   - Publishable Key → `STRIPE_PUBLISHABLE_KEY`
   - Secret Key → `STRIPE_SECRET_KEY`
5. Go to Developers → Webhooks
6. Create endpoint: `https://yourdomain.com/api/v1/payments/webhook/`
7. Copy Signing Secret → `STRIPE_WEBHOOK_SECRET`

### Django Secret Key

Generate a secure secret key:

```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

Copy output to `.env`

---

## 🧪 Verify Installation

### Run Tests

```bash
python manage.py test
```

### Check Database

```bash
python manage.py dbshell

# List tables
\dt

# Check users table
SELECT * FROM users_customuser;

# Exit
\q
```

### Test API

```bash
# Get all products
curl http://127.0.0.1:8000/api/v1/products/

# Create order
curl -X POST http://127.0.0.1:8000/api/v1/orders/ \
  -H "Content-Type: application/json" \
  -d '{"user": 1, "total_price": 50000}'
```

### Test Bot

Send `/start` to your bot in Telegram.

---

## 🆘 Troubleshooting

### PostgreSQL Connection Error

```
Error: could not connect to server: No such file or directory
```

**Solution:**
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Start PostgreSQL
sudo systemctl start postgresql

# On macOS
brew services start postgresql@14
```

### Migration Error

```
django.db.utils.ProgrammingError: relation does not exist
```

**Solution:**
```bash
python manage.py migrate --run-syncdb
python manage.py migrate
```

### Bot Not Responding

**Solution:**
```bash
# Check if bot is running
ps aux | grep runbot

# Check logs
tail -f logs/telegram_bot.log

# Restart bot
python tgbot/tgb/runbot.py
```

### Static Files Not Loading

**Solution:**
```bash
python manage.py collectstatic --noinput --clear
```

### Port Already in Use

**Solution:**
```bash
# On Linux/macOS
lsof -i :8000
kill -9 <PID>

# On Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Database Password Error

**Solution:**
```bash
# Reset PostgreSQL password
sudo -u postgres psql
\password salesbot_user
# Enter new password
\q
```

---

## 📦 Production Deployment

### Option 1: DigitalOcean

1. Create Ubuntu droplet
2. SSH into server
3. Follow local setup (Steps 1-9)
4. Set `DEBUG=False` in `.env`
5. Configure Nginx
6. Set up SSL certificate

### Option 2: Heroku

```bash
# Install Heroku CLI
# Login
heroku login

# Create app
heroku create salesbot-app

# Set environment variables
heroku config:set DEBUG=False
heroku config:set DJANGO_SECRET_KEY=your-key

# Deploy
git push heroku main

# Run migrations
heroku run python manage.py migrate
```

### Option 3: AWS

1. Create EC2 instance (Ubuntu 20.04)
2. Configure security groups
3. Install dependencies
4. Follow setup steps
5. Use RDS for PostgreSQL
6. Use Elastic IP
7. Set up CloudFront CDN

### Security Checklist

- [ ] Set `DEBUG=False`
- [ ] Use strong `DJANGO_SECRET_KEY`
- [ ] Enable HTTPS
- [ ] Set secure cookie flags
- [ ] Configure CORS
- [ ] Set up firewall
- [ ] Enable 2FA
- [ ] Regular backups
- [ ] Monitor logs
- [ ] Update dependencies

---

## 🔒 Security Setup

### Enable HTTPS

```env
DEBUG=False
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### Create SSL Certificate

```bash
# Using Let's Encrypt
sudo apt-get install certbot
sudo certbot certonly --standalone -d yourdomain.com
```

### Configure Firewall

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow http
sudo ufw allow https
sudo ufw enable
```

---

## 📚 Next Steps

1. **Configure Stripe Webhook** - [Guide](https://stripe.com/docs/webhooks/setup)
2. **Set up Admin Dashboard** - Login to `http://localhost:8000/admin`
3. **Add Products** - Use admin panel or API
4. **Test Payment Flow** - Use Stripe test cards
5. **Deploy to Production** - Choose deployment option
6. **Monitor Performance** - Set up logging and monitoring

---

## 💬 Need Help?

- 📖 [Documentation](docs/)
- 🐛 [Report Issue](https://github.com/yourusername/salesbot/issues)
- 💬 [Discussions](https://github.com/yourusername/salesbot/discussions)
- 📧 [Email Support](mailto:support@salesbot.example.com)
- 🗨️ [Telegram Group](https://t.me/salesbot_community)

---

<div align="center">

**Happy Building! 🚀**

Once installed, check the [README](README.md) for usage guide.

</div>
