# SmartForce Training System Guide

## Overview

The SmartForce training system allows professors to create structured workouts for specific users. Each training consists of multiple exercises with specific sets and repetitions.

## System Structure

### Training Structure
```
Training A
├── Exercise: Dumbbell Press
│   ├── Sets: 4
│   └── Repetitions: 12
├── Exercise: Squats
│   ├── Sets: 3
│   └── Repetitions: 15
└── Exercise: Plank
    ├── Sets: 3
    └── Repetitions: 60 seconds
```

## API Endpoints

### Exercise Catalog Management

#### 1. Get Exercise Catalog
```http
GET /api/v1/exercises/
Authorization: Bearer <token>
```

**Query Parameters:**
- `skip`: Number of records to skip (pagination)
- `limit`: Maximum number of records to return
- `name`: Filter exercises by name (partial match)

**Response:**
```json
[
  {
    "id": 1,
    "name": "Dumbbell Press",
    "description": "Chest exercise using dumbbells for strength and muscle building",
    "created_at": "2025-07-10T15:30:00"
  },
  {
    "id": 2,
    "name": "Squats",
    "description": "Lower body exercise targeting quadriceps, hamstrings, and glutes",
    "created_at": "2025-07-10T15:30:00"
  }
]
```

#### 2. Create New Exercise
```http
POST /api/v1/exercises/
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "New Exercise",
  "description": "Description of the exercise"
}
```

#### 3. Get Exercise by ID
```http
GET /api/v1/exercises/{exercise_id}
Authorization: Bearer <token>
```

### Training Management

#### 1. Create Training for Specific User
```http
POST /api/v1/trainings/
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "Upper Body Strength",
  "description": "Focus on chest, shoulders, and arms",
  "user_id": 1,
  "professor_id": 2,
  "exercises": [
    {
      "exercise_id": 1,
      "sets": 4,
      "repetitions": 12
    },
    {
      "exercise_id": 5,
      "sets": 3,
      "repetitions": 10
    },
    {
      "exercise_id": 9,
      "sets": 3,
      "repetitions": 15
    }
  ]
}
```

**Response:**
```json
{
  "id": 1,
  "name": "Upper Body Strength",
  "description": "Focus on chest, shoulders, and arms",
  "user_id": 1,
  "professor_id": 2,
  "created_at": "2025-07-10T15:30:00",
  "exercises": [
    {
      "id": 1,
      "exercise_id": 1,
      "sets": 4,
      "repetitions": 12,
      "exercise_name": "Dumbbell Press",
      "exercise_description": "Chest exercise using dumbbells for strength and muscle building"
    },
    {
      "id": 2,
      "exercise_id": 5,
      "sets": 3,
      "repetitions": 10,
      "exercise_name": "Pull-ups",
      "exercise_description": "Upper body exercise targeting back and biceps"
    },
    {
      "id": 3,
      "exercise_id": 9,
      "sets": 3,
      "repetitions": 15,
      "exercise_name": "Bicep Curls",
      "exercise_description": "Isolation exercise for bicep development"
    }
  ]
}
```

#### 2. Get Training by ID
```http
GET /api/v1/trainings/{training_id}
Authorization: Bearer <token>
```

#### 3. Get User's Trainings
```http
GET /api/v1/users/{user_id}/trainings
Authorization: Bearer <token>
```

#### 4. Get Professor's Created Trainings
```http
GET /api/v1/professors/{professor_id}/trainings
Authorization: Bearer <token>
```

## Setup Instructions

### 1. Populate Exercise Catalog

Run the exercise population script to add sample exercises:

```bash
python scripts/populate_exercises.py
```

This will create 15 common exercises in the database.

### 2. Create Training Workflow

1. **Professor logs in** and gets authentication token
2. **Professor views exercise catalog** to see available exercises
3. **Professor creates training** for specific user with selected exercises
4. **User can view their trainings** with complete exercise details

### 3. Example Training Creation

```python
import requests

# Authentication
headers = {"Authorization": "Bearer <your_token>"}

# Get available exercises
exercises_response = requests.get("http://localhost:8000/api/v1/exercises/", headers=headers)
exercises = exercises_response.json()

# Create training
training_data = {
    "name": "Full Body Workout",
    "description": "Complete body workout for strength",
    "user_id": 1,
    "professor_id": 2,
    "exercises": [
        {"exercise_id": 1, "sets": 4, "repetitions": 12},  # Dumbbell Press
        {"exercise_id": 2, "sets": 3, "repetitions": 15},  # Squats
        {"exercise_id": 8, "sets": 3, "repetitions": 60}   # Plank (60 seconds)
    ]
}

response = requests.post(
    "http://localhost:8000/api/v1/trainings/",
    json=training_data,
    headers=headers
)

training = response.json()
print(f"Created training: {training['name']}")
```

## Features

- ✅ **Exercise Catalog**: Professors can manage exercise library
- ✅ **Structured Trainings**: Each training has multiple exercises with sets/reps
- ✅ **User-Specific**: Trainings are created for specific users
- ✅ **Professor Management**: Professors can create and manage trainings
- ✅ **Detailed Responses**: Training responses include exercise names and descriptions
- ✅ **Access Control**: Users can only access their own trainings
- ✅ **Rate Limiting**: API endpoints are protected with rate limiting
- ✅ **Caching**: Training data is cached for better performance

## Database Schema

### Exercises Table
- `id`: Primary key
- `name`: Exercise name
- `description`: Exercise description
- `created_at`: Creation timestamp

### Trainings Table
- `id`: Primary key
- `name`: Training name
- `description`: Training description
- `user_id`: Foreign key to users table
- `professor_id`: Foreign key to professors table
- `created_at`: Creation timestamp

### Training_Exercises Table
- `id`: Primary key
- `training_id`: Foreign key to trainings table
- `exercise_id`: Foreign key to exercises table
- `sets`: Number of sets
- `repetitions`: Number of repetitions

This structure allows for flexible training creation with multiple exercises per training, each with their own sets and repetitions configuration. 