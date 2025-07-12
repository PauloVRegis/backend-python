# 🔐 SmartForce Authentication Guide

## Overview

This guide explains how to get and use Bearer tokens in your SmartForce application for accessing protected API endpoints.

## 🚀 Quick Start

### 1. Start the Application
```bash
./start_dev.sh
```

### 2. Test Authentication (Automatic)
```bash
python scripts/test_auth.py
```

This script will:
- Register a test user
- Login and get a bearer token
- Test protected endpoints
- Show usage examples

---

## 📋 Manual Authentication Steps

### Step 1: Register a User

**Endpoint:** `POST /api/v1/auth/register`

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "name": "John Doe",
    "password": "securepassword123"
  }'
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "name": "John Doe",
  "created_at": "2025-07-10T15:30:00"
}
```

### Step 2: Login to Get Bearer Token

**Endpoint:** `POST /api/v1/auth/login/json`

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login/json" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }'
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800,
  "user_id": 1,
  "email": "user@example.com"
}
```

### Step 3: Use Bearer Token

**Store the token:**
```bash
export TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Use in API calls:**
```bash
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer $TOKEN"
```

---

## 🔧 Available Authentication Endpoints

### 1. Register User
```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "name": "User Name",
  "password": "password123"
}
```

### 2. Login (Form Data - OAuth2 Standard)
```http
POST /api/v1/auth/login
Content-Type: application/x-www-form-urlencoded

username=user@example.com&password=password123
```

### 3. Login (JSON - Easier for Testing)
```http
POST /api/v1/auth/login/json
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

### 4. Get Current User Info
```http
GET /api/v1/auth/me
Authorization: Bearer <token>
```

### 5. Refresh Token
```http
POST /api/v1/auth/refresh
Authorization: Bearer <token>
```

---

## 🛡️ Using Bearer Tokens

### Header Format
```
Authorization: Bearer <your_token_here>
```

### Example API Calls

#### 1. Get Exercise Catalog
```bash
curl -X GET "http://localhost:8000/api/v1/exercises/" \
  -H "Authorization: Bearer $TOKEN"
```

#### 2. Create Training
```bash
curl -X POST "http://localhost:8000/api/v1/trainings/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Upper Body Workout",
    "description": "Focus on chest and arms",
    "user_id": 1,
    "professor_id": 1,
    "exercises": [
      {
        "exercise_id": 1,
        "sets": 4,
        "repetitions": 12
      }
    ]
  }'
```

#### 3. Get User's Trainings
```bash
curl -X GET "http://localhost:8000/api/v1/users/1/trainings" \
  -H "Authorization: Bearer $TOKEN"
```

#### 4. Get Training by ID
```bash
curl -X GET "http://localhost:8000/api/v1/trainings/1" \
  -H "Authorization: Bearer $TOKEN"
```

---

## 🔄 Token Management

### Token Expiration
- **Default expiration:** 30 minutes
- **Configurable:** Set `ACCESS_TOKEN_EXPIRE_MINUTES` in environment

### Refresh Token
When your token expires, use the refresh endpoint:
```bash
curl -X POST "http://localhost:8000/api/v1/auth/refresh" \
  -H "Authorization: Bearer $TOKEN"
```

### Token Validation
The system automatically validates tokens on protected endpoints. Invalid tokens return:
```json
{
  "detail": "Could not validate credentials"
}
```

---

## 🧪 Testing with Python

### Using requests library
```python
import requests

# Login
login_data = {
    "email": "user@example.com",
    "password": "password123"
}

response = requests.post(
    "http://localhost:8000/api/v1/auth/login/json",
    json=login_data
)

if response.status_code == 200:
    token_data = response.json()
    bearer_token = token_data['access_token']
    
    # Use token for API calls
    headers = {"Authorization": f"Bearer {bearer_token}"}
    
    # Get exercises
    exercises_response = requests.get(
        "http://localhost:8000/api/v1/exercises/",
        headers=headers
    )
    
    print(exercises_response.json())
```

### Using the test script
```bash
# Run the automated test
python scripts/test_auth.py

# This will:
# 1. Register a test user
# 2. Login and get token
# 3. Test protected endpoints
# 4. Show usage examples
```

---

## 🔒 Security Features

### JWT Token Security
- **Algorithm:** HS256 (HMAC with SHA-256)
- **Secret Key:** Configurable via `SECRET_KEY` environment variable
- **Expiration:** Automatic token expiration
- **Validation:** Server-side token validation

### Password Security
- **Hashing:** Bcrypt with salt
- **Verification:** Secure password comparison
- **Storage:** Only hashed passwords stored

### Rate Limiting
- **Login attempts:** Limited to prevent brute force
- **API calls:** Rate limited per endpoint
- **Protection:** DDoS and abuse prevention

---

## 🚨 Troubleshooting

### Common Issues

#### 1. "Could not validate credentials"
- **Cause:** Invalid or expired token
- **Solution:** Login again to get a new token

#### 2. "Incorrect email or password"
- **Cause:** Wrong credentials
- **Solution:** Check email and password

#### 3. "Email already registered"
- **Cause:** User already exists
- **Solution:** Use login instead of register

#### 4. Connection refused
- **Cause:** Application not running
- **Solution:** Start with `./start_dev.sh`

### Debug Mode
Enable debug mode for detailed error messages:
```bash
export DEBUG=true
./start_dev.sh
```

---

## 📚 API Documentation

Once the application is running, visit:
- **Interactive API Docs:** http://localhost:8000/docs
- **Alternative Docs:** http://localhost:8000/redoc

These provide:
- Interactive testing interface
- Automatic token authentication
- Request/response examples
- Schema documentation

---

## 🎯 Next Steps

1. **Start the application:** `./start_dev.sh`
2. **Run authentication test:** `python scripts/test_auth.py`
3. **Create your first training** using the bearer token
4. **Explore the API documentation** at http://localhost:8000/docs

Your SmartForce application is now ready for authenticated API access! 🚀 