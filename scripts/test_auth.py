#!/usr/bin/env python3
"""
Script to test authentication and get bearer tokens
"""

import requests
import json

# API base URL
BASE_URL = "http://localhost:8000/api/v1"

def test_authentication():
    """Test the complete authentication flow"""
    
    print("🔐 Testing SmartForce Authentication System")
    print("=" * 50)
    
    # Test data
    test_user = {
        "email": "test@example.com",
        "name": "Test User",
        "password": "testpassword123"
    }
    
    # Step 1: Register a new user
    print("\n1️⃣ Registering new user...")
    try:
        register_response = requests.post(
            f"{BASE_URL}/register",
            json=test_user
        )
        
        if register_response.status_code == 200:
            user_data = register_response.json()
            print(f"✅ User registered successfully!")
            print(f"   User ID: {user_data['id']}")
            print(f"   Email: {user_data['email']}")
            print(f"   Name: {user_data['name']}")
        elif register_response.status_code == 400:
            print("ℹ️ User already exists, proceeding to login...")
        else:
            print(f"❌ Registration failed: {register_response.status_code}")
            print(f"   Response: {register_response.text}")
            return
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure the application is running!")
        print("   Run: ./start_dev.sh")
        return
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return
    
    # Step 2: Login to get bearer token
    print("\n2️⃣ Logging in to get bearer token...")
    try:
        login_data = {
            "email": test_user["email"],
            "password": test_user["password"]
        }
        
        login_response = requests.post(
            f"{BASE_URL}/login/json",
            json=login_data
        )
        
        if login_response.status_code == 200:
            token_data = login_response.json()
            print("✅ Login successful!")
            print(f"   Access Token: {token_data['access_token'][:50]}...")
            print(f"   Token Type: {token_data['token_type']}")
            print(f"   Expires In: {token_data['expires_in']} seconds")
            print(f"   User ID: {token_data['user_id']}")
            print(f"   Email: {token_data['email']}")
            
            # Store token for further use
            bearer_token = token_data['access_token']
            
            # Step 3: Test protected endpoint
            print("\n3️⃣ Testing protected endpoint...")
            headers = {"Authorization": f"Bearer {bearer_token}"}
            
            me_response = requests.get(
                f"{BASE_URL}/me",
                headers=headers
            )
            
            if me_response.status_code == 200:
                user_info = me_response.json()
                print("✅ Protected endpoint works!")
                print(f"   Current user: {user_info['name']} ({user_info['email']})")
            else:
                print(f"❌ Protected endpoint failed: {me_response.status_code}")
                print(f"   Response: {me_response.text}")
            
            # Step 4: Test exercise catalog
            print("\n4️⃣ Testing exercise catalog...")
            exercises_response = requests.get(
                f"{BASE_URL}/exercises/",
                headers=headers
            )
            
            if exercises_response.status_code == 200:
                exercises = exercises_response.json()
                print(f"✅ Exercise catalog accessible!")
                print(f"   Found {len(exercises)} exercises")
                if exercises:
                    print(f"   First exercise: {exercises[0]['name']}")
            else:
                print(f"❌ Exercise catalog failed: {exercises_response.status_code}")
                print(f"   Response: {exercises_response.text}")
            
            print("\n🎉 Authentication test completed successfully!")
            print("\n📋 Summary:")
            print(f"   Bearer Token: {bearer_token}")
            print(f"   Use this token in Authorization header: Bearer {bearer_token}")
            
        else:
            print(f"❌ Login failed: {login_response.status_code}")
            print(f"   Response: {login_response.text}")
            
    except Exception as e:
        print(f"❌ Login error: {e}")

def show_usage_examples():
    """Show usage examples with the bearer token"""
    print("\n" + "=" * 50)
    print("📖 Usage Examples with Bearer Token")
    print("=" * 50)
    
    print("\n1️⃣ Get Exercise Catalog:")
    print("""
curl -X GET "http://localhost:8000/api/v1/exercises/" \\
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
    """)
    
    print("\n2️⃣ Create Training:")
    print("""
curl -X POST "http://localhost:8000/api/v1/trainings/" \\
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \\
  -H "Content-Type: application/json" \\
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
      },
      {
        "exercise_id": 5,
        "sets": 3,
        "repetitions": 10
      }
    ]
  }'
    """)
    
    print("\n3️⃣ Get User's Trainings:")
    print("""
curl -X GET "http://localhost:8000/api/v1/trainings/user/1" \\
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
    """)

if __name__ == "__main__":
    test_authentication()
    show_usage_examples() 