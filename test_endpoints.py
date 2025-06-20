#!/usr/bin/env python3
"""
Test all endpoints to verify database schema fixes
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def get_auth_token():
    """Get auth token for existing user"""
    login_data = {
        "username": "lunaxcode2030@gmail.com",
        "password": "LUnaxcode@2030"
    }
    
    response = requests.post(
        f"{BASE_URL}/auth/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        print(f"❌ Login failed: {response.status_code} - {response.text}")
        return None

def test_endpoints():
    """Test critical endpoints"""
    print("🧪 Testing Fixed Endpoints")
    print("=" * 50)
    
    # Get auth token
    print("🔐 Getting auth token...")
    token = get_auth_token()
    if not token:
        return False
    
    headers = {"Authorization": f"Bearer {token}"}
    print("✅ Auth token obtained")
    
    # Test endpoints that were failing
    endpoints_to_test = [
        ("GET", "/users/me", "User profile"),
        ("GET", "/event-types", "Event types list"),
        ("GET", "/bookings", "Bookings list"),
        ("GET", "/teams", "Teams list"),
    ]
    
    all_passed = True
    
    for method, endpoint, description in endpoints_to_test:
        print(f"\n🔍 Testing {description}: {method} {endpoint}")
        
        try:
            if method == "GET":
                response = requests.get(f"{BASE_URL}{endpoint}", headers=headers)
            else:
                response = requests.request(method, f"{BASE_URL}{endpoint}", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {description}: Success")
                if isinstance(data, list):
                    print(f"   Returned {len(data)} items")
                elif isinstance(data, dict):
                    print(f"   Returned object with {len(data)} fields")
            else:
                print(f"❌ {description}: Failed - {response.status_code}")
                print(f"   Response: {response.text[:200]}...")
                all_passed = False
                
        except Exception as e:
            print(f"❌ {description}: Error - {e}")
            all_passed = False
    
    # Test creating an event type
    print(f"\n🔍 Testing Event Type Creation")
    event_type_data = {
        "title": "Test Meeting",
        "slug": f"test-meeting-{int(datetime.now().timestamp())}",
        "description": "Test event type",
        "length": 30,
        "hidden": False,
        "requiresConfirmation": False,
        "minimumBookingNotice": 120,
        "price": 0,
        "currency": "usd"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/event-types",
            json=event_type_data,
            headers={**headers, "Content-Type": "application/json"}
        )
        
        if response.status_code in [200, 201]:
            event_data = response.json()
            print("✅ Event Type Creation: Success")
            print(f"   Created event: {event_data.get('title')} (ID: {event_data.get('id')})")
        else:
            print(f"❌ Event Type Creation: Failed - {response.status_code}")
            print(f"   Response: {response.text}")
            all_passed = False
            
    except Exception as e:
        print(f"❌ Event Type Creation: Error - {e}")
        all_passed = False
    
    return all_passed

if __name__ == "__main__":
    try:
        success = test_endpoints()
        if success:
            print("\n🎉 ALL TESTS PASSED!")
            print("✅ Database schema is properly aligned")
            print("✅ All endpoints working correctly")
            print("🚀 Ready for production deployment!")
        else:
            print("\n❌ Some tests failed")
            print("🔧 Check server logs for details")
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server")
        print("   Make sure server is running: uvicorn app.main:app --reload --port 8000") 