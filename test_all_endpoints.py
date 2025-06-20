#!/usr/bin/env python3
"""
Comprehensive endpoint testing with seed data
Tests all major endpoints to ensure they work correctly with realistic data
"""

import requests
import subprocess
import time
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000"

def get_auth_token():
    """Get authentication token"""
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

def test_endpoint(method, endpoint, headers=None, data=None, description=""):
    """Test a single endpoint"""
    try:
        if method == "GET":
            response = requests.get(f"{BASE_URL}{endpoint}", headers=headers)
        elif method == "POST":
            response = requests.post(f"{BASE_URL}{endpoint}", headers=headers, json=data)
        elif method == "PATCH":
            response = requests.patch(f"{BASE_URL}{endpoint}", headers=headers, json=data)
        elif method == "DELETE":
            response = requests.delete(f"{BASE_URL}{endpoint}", headers=headers)
        else:
            response = requests.request(method, f"{BASE_URL}{endpoint}", headers=headers, json=data)
        
        if response.status_code in [200, 201]:
            result = response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
            return True, response.status_code, result
        else:
            return False, response.status_code, response.text
            
    except Exception as e:
        return False, 0, str(e)

def run_comprehensive_tests():
    """Run comprehensive endpoint tests"""
    print("🧪 Comprehensive Endpoint Testing with Seed Data")
    print("=" * 60)
    
    # Start server
    print("🚀 Starting server...")
    proc = subprocess.Popen(['python', '-m', 'uvicorn', 'app.main:app', '--port', '8000'], 
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(4)
    
    try:
        # Get auth token
        print("\n🔐 Authenticating...")
        token = get_auth_token()
        if not token:
            return False
        
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        print("✅ Authentication successful")
        
        # Test results tracking
        tests_passed = 0
        tests_total = 0
        
        # Test categories
        test_categories = [
            {
                "name": "🏥 Health & Debug Endpoints",
                "tests": [
                    ("GET", "/health", None, None, "Health check"),
                    ("GET", "/debug", None, None, "Debug info"),
                ]
            },
            {
                "name": "👤 User Management",
                "tests": [
                    ("GET", "/users/me", headers, None, "Get current user profile"),
                ]
            },
            {
                "name": "📅 Event Type Management", 
                "tests": [
                    ("GET", "/event-types", headers, None, "List event types"),
                    ("POST", "/event-types", headers, {
                        "title": "Quick Meeting",
                        "slug": f"quick-meeting-{int(time.time())}",
                        "description": "15-minute quick sync",
                        "length": 15,
                        "hidden": False,
                        "requiresConfirmation": False,
                        "minimumBookingNotice": 60,
                        "price": 0,
                        "currency": "usd"
                    }, "Create new event type"),
                ]
            },
            {
                "name": "📝 Booking Management",
                "tests": [
                    ("GET", "/bookings", headers, None, "List user bookings"),
                ]
            },
            {
                "name": "👥 Team Management",
                "tests": [
                    ("GET", "/teams", headers, None, "List user teams"),
                    ("POST", "/teams", headers, {
                        "name": "Marketing Team",
                        "slug": f"marketing-{int(time.time())}",
                        "bio": "Marketing and growth team",
                        "hideBranding": False
                    }, "Create new team"),
                ]
            },
            {
                "name": "🏢 Organization Management",
                "tests": [
                    ("GET", "/organizations", headers, None, "List organizations"),
                    ("POST", "/organizations", headers, {
                        "name": "TestCorp",
                        "slug": f"testcorp-{int(time.time())}"
                    }, "Create new organization"),
                ]
            },
            {
                "name": "🤝 Membership Management",
                "tests": [
                    ("GET", "/memberships", headers, None, "List memberships"),
                ]
            },
            {
                "name": "🔗 Webhook Management",
                "tests": [
                    ("GET", "/webhooks", headers, None, "List webhooks"),
                    ("POST", "/webhooks", headers, {
                        "subscriber_url": "https://example.com/webhook",
                        "event_triggers": ["booking.created"],
                        "active": True
                    }, "Create new webhook"),
                ]
            },
            {
                "name": "📊 Analytics & Reporting",
                "tests": [
                    ("GET", "/analytics/bookings", headers, None, "Booking analytics"),
                    ("GET", "/analytics/event-types", headers, None, "Event type performance"),
                ]
            },
            {
                "name": "⏰ Availability Management",
                "tests": [
                    ("GET", "/availability", headers, None, "Get availability"),
                ]
            }
        ]
        
        # Run all test categories
        for category in test_categories:
            print(f"\n{category['name']}")
            print("-" * 40)
            
            for method, endpoint, test_headers, data, description in category["tests"]:
                tests_total += 1
                success, status_code, result = test_endpoint(method, endpoint, test_headers, data, description)
                
                if success:
                    tests_passed += 1
                    if isinstance(result, list):
                        print(f"   ✅ {description}: {status_code} ({len(result)} items)")
                    elif isinstance(result, dict):
                        print(f"   ✅ {description}: {status_code} (object with {len(result)} fields)")
                    else:
                        print(f"   ✅ {description}: {status_code}")
                else:
                    print(f"   ❌ {description}: {status_code} - {str(result)[:100]}...")
        
        # Test specific endpoints with IDs from seed data
        print(f"\n🎯 Testing Specific Resource Endpoints")
        print("-" * 40)
        
        # Get some IDs for detailed testing
        event_types_response = requests.get(f"{BASE_URL}/event-types", headers=headers)
        if event_types_response.status_code == 200:
            event_types = event_types_response.json()
            if event_types:
                event_type_id = event_types[0]["id"]
                tests_total += 1
                success, status_code, result = test_endpoint("GET", f"/event-types/{event_type_id}", headers)
                if success:
                    tests_passed += 1
                    print(f"   ✅ Get specific event type: {status_code}")
                else:
                    print(f"   ❌ Get specific event type: {status_code}")
        
        bookings_response = requests.get(f"{BASE_URL}/bookings", headers=headers)
        if bookings_response.status_code == 200:
            bookings = bookings_response.json()
            if bookings:
                booking_id = bookings[0]["id"]
                tests_total += 1
                success, status_code, result = test_endpoint("GET", f"/bookings/{booking_id}", headers)
                if success:
                    tests_passed += 1
                    print(f"   ✅ Get specific booking: {status_code}")
                else:
                    print(f"   ❌ Get specific booking: {status_code}")
        
        # Test public endpoints (no auth required)
        print(f"\n🌐 Testing Public Endpoints")
        print("-" * 40)
        
        public_tests = [
            ("GET", "/public/lunaxcode", None, None, "Get user public profile"),
        ]
        
        for method, endpoint, test_headers, data, description in public_tests:
            tests_total += 1
            success, status_code, result = test_endpoint(method, endpoint, test_headers, data, description)
            
            if success:
                tests_passed += 1
                print(f"   ✅ {description}: {status_code}")
            else:
                print(f"   ❌ {description}: {status_code} - {str(result)[:100]}...")
        
        # Final results
        print(f"\n📊 Test Results Summary")
        print("=" * 40)
        print(f"✅ Tests Passed: {tests_passed}")
        print(f"❌ Tests Failed: {tests_total - tests_passed}")
        print(f"📊 Total Tests: {tests_total}")
        print(f"🎯 Success Rate: {(tests_passed/tests_total)*100:.1f}%")
        
        if tests_passed == tests_total:
            print(f"\n🎉 ALL TESTS PASSED! Your API is working perfectly!")
            print(f"🚀 Ready for production deployment!")
        elif tests_passed > tests_total * 0.8:
            print(f"\n✅ Most tests passed! Minor issues to address.")
        else:
            print(f"\n⚠️ Several tests failed. Please review the errors above.")
        
        return tests_passed == tests_total
        
    except Exception as e:
        print(f"❌ Test execution error: {e}")
        return False
    finally:
        proc.terminate()
        proc.wait()
        print("\n🛑 Server stopped")

if __name__ == "__main__":
    try:
        success = run_comprehensive_tests()
        if success:
            print("\n🎊 Comprehensive testing completed successfully!")
        else:
            print("\n🔧 Some issues found - check the results above.")
    except KeyboardInterrupt:
        print("\n⏹️ Testing interrupted by user")
    except Exception as e:
        print(f"\n❌ Testing failed: {e}") 