# Banking System

A comprehensive digital banking management system built with Python, FastAPI, and PostgreSQL.

## Features

- User authentication with JWT tokens
- Multiple account types (Savings, Checking, Credit)
- Transaction management (Deposit, Withdrawal, Transfer)
- Real-time balance tracking
- Secure password hashing
- RESTful API with automatic documentation

## Tech Stack

- **Backend**: FastAPI
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT (JSON Web Tokens)
- **Migration**: Alembic
- **Testing**: Pytest

##� Prerequisites

- Python 3.10+
- PostgreSQL 14+
- pip

## Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/banking-system.git
cd banking-system
```

2. Create virtual environment:
```bash
python -m venv banking_env
source banking_env/bin/activate  # On Windows: banking_env\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your database credentials
```

5. Set up database:
```bash
createdb banking_db
alembic upgrade head
```

6. Run the application:
```bash
uvicorn app.main:app --reload
```

7. Access the API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user

### Accounts
- `POST /api/v1/accounts/` - Create account
- `GET /api/v1/accounts/` - Get user accounts
- `GET /api/v1/accounts/{id}` - Get account details

### Transactions
- `POST /api/v1/transactions/` - Create transaction
- `GET /api/v1/transactions/` - Get user transactions
- `GET /api/v1/transactions/{id}` - Get transaction details

## Security

- Passwords are hashed using bcrypt
- JWT tokens for authentication
- SQL injection prevention with SQLAlchemy ORM
- Environment variables for sensitive data

## License

This project is open source and available under the MIT License.

## Author

Mayank Raj - [GitHub](https://github.com/YOUR_USERNAME)

(user - banking_user
password - Mayank1365)

