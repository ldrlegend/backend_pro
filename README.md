# FastAPI Backend Project

A FastAPI-based backend application with user management and authentication.

## Prerequisites

1. **Install Python**: Download and install Python 3.8+ from [python.org](https://www.python.org/downloads/)
2. **Install Git**: Download and install Git from [git-scm.com](https://git-scm.com/)

## Setup Instructions

### 1. Install Python
- Download Python from [python.org](https://www.python.org/downloads/)
- During installation, make sure to check "Add Python to PATH"
- Verify installation by running: `python --version`

### 2. Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the root directory:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/database_name
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 5. Database Setup
```bash
# Initialize database (if using SQLite for development)
python -c "from app.db.init_db import init_db; init_db()"
```

### 6. Run the Application
```bash
python run.py
```

The application will be available at `http://localhost:8000`

## API Documentation
- Interactive API docs: `http://localhost:8000/docs`
- ReDoc documentation: `http://localhost:8000/redoc`

## Project Structure
```
backend_pro/
├── app/
│   ├── api/v1/          # API routes
│   ├── db/              # Database configuration
│   ├── models/          # SQLAlchemy models
│   ├── schemas/         # Pydantic schemas
│   └── main.py          # FastAPI application
├── requirements.txt     # Python dependencies
├── run.py              # Application entry point
└── README.md           # This file
```

### 6. Docker

- Docker build
docker build -t product-mana-be:latest .

- Docker run with db info
docker run -d --name product-mana-be -p 8003:8003 `
  -e DB_HOST=host.docker.internal `
  -e DB_PORT=5432 `
  -e DB_NAME=mydb `
  -e DB_USER=postgres `
  -e DB_PASSWORD=password `
  product-mana-be:latest