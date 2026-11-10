# 🤝 Contributing to SalesBot

First off, thank you for considering contributing to SalesBot! It's people like you that make SalesBot such a great tool.

## 📋 Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

### Our Standards

Examples of behavior that contributes to creating a positive environment include:

- ✅ Using welcoming and inclusive language
- ✅ Being respectful of differing opinions, viewpoints, and experiences
- ✅ Giving and gracefully accepting constructive criticism
- ✅ Focusing on what is best for the community
- ✅ Showing empathy towards other community members

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- PostgreSQL 13+
- Docker (optional)
- Git

### Development Setup

1. **Fork and clone the repository**
```bash
git clone https://github.com/yourusername/salesbot.git
cd salesbot
```

2. **Create development branch**
```bash
git checkout -b feature/your-feature-name
```

3. **Set up virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

4. **Configure development environment**
```bash
cp .env.example .env
# Edit .env for local development
```

5. **Run migrations**
```bash
python manage.py migrate
python manage.py createsuperuser
```

6. **Start development server**
```bash
python manage.py runserver
```

---

## 🔄 Development Workflow

### 1. Create Feature Branch
```bash
git checkout -b feature/your-feature-name
```

**Branch naming convention:**
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation
- `refactor/` - Code refactoring
- `test/` - Test improvements

### 2. Make Changes

Follow the coding standards:

#### Python Code Style
```python
# Use PEP 8 standard
# Good
def calculate_order_total(items):
    """Calculate total price of order items."""
    total = sum(item.price * item.quantity for item in items)
    return total

# Avoid
def calc_total(items):
    return sum([i.price * i.quantity for i in items])
```

#### Django Models
```python
class Order(models.Model):
    """Model representing a customer order."""
    
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default='Pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
    
    def __str__(self):
        return f'Order #{self.id} - {self.user.full_name}'
```

#### Telegram Bot Handlers
```python
def handle_start_command(update, context):
    """Handle /start command."""
    chat_id = update.message.chat_id
    user = get_or_create_user(chat_id)
    
    send_welcome_message(update, user)
    logger.info(f"User {chat_id} started bot")
```

### 3. Write Tests

```python
# tests.py
from django.test import TestCase
from tgbot.models import Order

class OrderModelTest(TestCase):
    def setUp(self):
        self.user = create_test_user()
    
    def test_order_creation(self):
        """Test creating an order."""
        order = Order.objects.create(
            user=self.user,
            total_price=50000
        )
        self.assertEqual(order.status, 'Pending')
        self.assertTrue(order.id)
    
    def test_order_string_representation(self):
        """Test order string representation."""
        order = Order.objects.create(
            user=self.user,
            total_price=50000
        )
        self.assertIn(str(order.id), str(order))
```

### 4. Commit Changes

```bash
git add .
git commit -m "feat: add order confirmation webhook"
```

**Commit message format:**
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `style:` - Code style (formatting, etc)
- `refactor:` - Code refactoring
- `perf:` - Performance improvement
- `test:` - Adding/updating tests
- `chore:` - Build/tooling changes

**Example:**
```
feat(payment): add Stripe webhook integration

- Implement webhook endpoint for payment events
- Add signature verification for security
- Update order status on successful payment
- Send Telegram notification to user

Closes #123
```

### 5. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

---

## ✅ Pull Request Guidelines

### Before Submitting

- [ ] Code follows the style guidelines
- [ ] New features include tests
- [ ] Documentation is updated
- [ ] No unnecessary console logs
- [ ] No debug print statements
- [ ] All tests pass locally
- [ ] Commit messages are descriptive

### PR Template

```markdown
## Description
Brief description of the changes.

## Type of Change
- [ ] New feature
- [ ] Bug fix
- [ ] Breaking change
- [ ] Documentation update

## Related Issue
Closes #(issue number)

## Testing
Describe how this was tested.

## Screenshots (if applicable)
Add screenshots for UI changes.

## Checklist
- [ ] Tests pass
- [ ] Documentation updated
- [ ] No breaking changes
```

---

## 🐛 Reporting Bugs

### Before Submitting a Bug Report

- Check the documentation
- Search existing issues
- Check if issue is reproducible

### How to Submit a Good Bug Report

```markdown
**Describe the bug:**
Clear description of the issue.

**To Reproduce:**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '...'
3. See error

**Expected behavior:**
What should happen.

**Screenshots:**
If applicable.

**Environment:**
- OS: Windows/Mac/Linux
- Python version: 3.9
- Django version: 4.0
- Other versions: ...

**Additional context:**
Any other context.
```

---

## 💡 Feature Requests

### Before Submitting

- Check if feature already exists
- Search feature requests
- Check the roadmap

### Submitting a Feature Request

```markdown
**Is your feature request related to a problem?**
Describe the problem.

**Describe the solution you'd like:**
Clear description of the feature.

**Describe alternatives:**
Other solutions you've considered.

**Additional context:**
Any other context.
```

---

## 📚 Documentation

### Updating Documentation

1. Keep documentation up-to-date
2. Use clear, concise language
3. Include code examples
4. Update CHANGELOG.md

### Documentation Style

```markdown
# Feature Name

## Overview
Brief overview of the feature.

## Usage

### Basic Example
```python
example_code()
```

### Advanced Usage
More complex examples.

## API Reference

### Function/Method Name
**Parameters:**
- `param1` (type): Description

**Returns:**
- Type: Description

**Raises:**
- Exception: When this happens

## See Also
- [Related docs]()
```

---

## 🧪 Testing Guidelines

### Test Coverage
- Aim for 80%+ code coverage
- Test happy paths
- Test edge cases
- Test error cases

### Running Tests

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test tgbot

# Run specific test class
python manage.py test tgbot.tests.OrderModelTest

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

### Test Structure

```python
class OrderPaymentTest(TestCase):
    """Test order payment processing."""
    
    def setUp(self):
        """Set up test data."""
        self.user = create_test_user()
        self.order = create_test_order(self.user)
    
    def test_payment_success_updates_order_status(self):
        """Test that successful payment updates order status."""
        # Arrange
        initial_status = self.order.status
        
        # Act
        process_payment(self.order)
        self.order.refresh_from_db()
        
        # Assert
        self.assertEqual(self.order.status, 'Accepted')
        self.assertNotEqual(initial_status, self.order.status)
    
    def tearDown(self):
        """Clean up after tests."""
        self.order.delete()
        self.user.delete()
```

---

## 🔍 Code Review Process

### For Reviewers

- ✅ Check code quality
- ✅ Verify tests are included
- ✅ Ensure documentation is updated
- ✅ Look for security issues
- ✅ Check performance implications
- ✅ Provide constructive feedback

### For Authors

- ✅ Respond to feedback promptly
- ✅ Make requested changes
- ✅ Ask for clarification if needed
- ✅ Thank reviewers for their time

---

## 🎓 Development Tips

### Useful Commands

```bash
# Format code
black tgbot/ payment/ users/ --line-length=88

# Check code quality
flake8 tgbot/ payment/ users/

# Type checking
mypy tgbot/ payment/ users/

# Run linter
pylint tgbot/ payment/ users/

# Create migrations
python manage.py makemigrations

# Show migration SQL
python manage.py sqlmigrate tgbot 0001

# Django shell
python manage.py shell

# Database shell
python manage.py dbshell
```

### Debugging

```python
# Use Django debug toolbar
# Check settings.py for configuration

# Print debugging
from django.conf import settings
if settings.DEBUG:
    print(f"Debug info: {variable}")

# Logging
import logging
logger = logging.getLogger(__name__)
logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
```

---

## 🎯 Development Roadmap

### Q1 2024
- [ ] Enhanced analytics dashboard
- [ ] Multi-vendor support
- [ ] Advanced search

### Q2 2024
- [ ] Mobile app
- [ ] Real-time notifications
- [ ] AI recommendations

### Q3 2024
- [ ] Multi-language expansion
- [ ] Advanced reporting
- [ ] Performance optimization

---

## 📞 Questions?

- 📖 Check documentation in `/docs`
- 💬 Open a discussion on GitHub
- 📧 Email: dev@salesbot.example.com
- 🗨️ Telegram: [@salesbot_dev](https://t.me/salesbot_dev)

---

## 📝 License

By contributing to SalesBot, you agree that your contributions will be licensed under its MIT License.

---

<div align="center">

Thank you for contributing! 🙏

Made with ❤️ by the SalesBot community

</div>
