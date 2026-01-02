# Paytm Clone

A digital wallet system built with FastAPI backend and JavaScript/HTML/CSS frontend. This project mimics the core functionality of Paytm, enabling users to manage wallets, send money, and process payments.

## Overview

Paytm Clone is a full-stack web application that demonstrates a complete digital payment system. It includes user authentication, wallet management, UPI-based payments, and transaction tracking with sorting capabilities.

## Features

- User authentication and management
- Digital wallet creation and management
- Send money functionality between users
- UPI payment support
- Transaction history with sorting
- JWT-based authentication
- CORS support for cross-origin requests
- Responsive frontend interface

## Technology Stack

### Backend
- Framework: FastAPI
- Database: SQLAlchemy ORM
- Authentication: JWT tokens
- Middleware: CORS

### Frontend
- HTML: Markup structure
- CSS: Styling and responsive design
- JavaScript: Client-side functionality and interactivity

## Project Structure

paytm/
├── app/
│   ├── config/          # Configuration settings
│   ├── database/        # Database connection and setup
│   ├── exceptions/      # Custom exception handling
│   ├── models/          # SQLAlchemy models
│   ├── repo/            # Repository layer
│   ├── routers/         # API route handlers
│   │   ├── user_router.py
│   │   ├── wallet_router.py
│   │   ├── payment_router.py
│   │   └── transaction_router.py
│   └── schemas/         # Pydantic schemas for validation
├── frontend/            # Frontend files
│   ├── html/            # HTML templates
│   ├── css/             # Stylesheets
│   └── js/              # JavaScript files
├── main.py              # FastAPI application entry point
└── .env                 # Environment variables

## API Endpoints

### User Routes
- POST /users/ - Create a new user
- GET /users/{user_id} - Get user details

### Wallet Routes
- POST /wallets/ - Create a wallet
- GET /wallets/{wallet_id} - Get wallet details

### Payment Routes
- POST /payments/ - Process payment
- GET /payments/{payment_id} - Get payment details

### Transaction Routes
- POST /transactions/ - Create transaction
- GET /transactions/ - Get transaction history with sorting

## Getting Started

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Modern web browser

### Installation

1. Clone the repository
git clone https://github.com/nikhilajjarapu6/paytm.git
cd paytm

2. Create a virtual environment (optional)
python -m venv venv
source venv/bin/activate

3. Install dependencies
pip install -r requirements.txt

4. Configure environment variables
Edit .env file with your settings including:
- Database URL
- JWT secret key
- Other configuration parameters

5. Run the application
uvicorn main:app --reload

The API will be available at http://localhost:8000
API documentation will be at http://localhost:8000/docs

## Usage

### Creating a User
POST /users/ with username, email, and password

### Creating a Wallet
POST /wallets/ with user_id and initial balance

### Sending Money
POST /payments/ with sender, receiver, and amount

## Recent Updates

- Added sorting methods for transactions
- Implemented UPI send functionality
- Fixed send money bug
- Added JWT authentication
- Enhanced frontend with improved UI

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.


## Author

Nikhil Ajjarapu (@nikhilajjarapu6)

## Support

For support, please open an issue in the GitHub repository.
