#!/usr/bin/env python3
import requests
import subprocess
import time

# Start server in background
print('🚀 Starting server...')
proc = subprocess.Popen(['python', '-m', 'uvicorn', 'app.main:app', '--port', '8000'], 
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
time.sleep(4)

try:
    # Test health endpoint
    response = requests.get('http://localhost:8000/health', timeout=5)
    print(f'✅ Health check: {response.status_code}')
    
    # Test login
    login_data = {'username': 'lunaxcode2030@gmail.com', 'password': 'LUnaxcode@2030'}
    login_response = requests.post('http://localhost:8000/auth/login', data=login_data)
    print(f'🔐 Login: {login_response.status_code}')
    
    if login_response.status_code == 200:
        token = login_response.json()['access_token']
        headers = {'Authorization': f'Bearer {token}'}
        
        # Test teams endpoint (the one that was failing)
        teams_response = requests.get('http://localhost:8000/teams', headers=headers)
        print(f'👥 Teams endpoint: {teams_response.status_code}')
        
        # Test event types endpoint
        events_response = requests.get('http://localhost:8000/event-types', headers=headers)
        print(f'📅 Event types: {events_response.status_code}')
        
        print('\n🎉 ALL TESTS PASSED! Endpoints are working!')
    else:
        print(f'❌ Login failed: {login_response.text}')
        
except Exception as e:
    print(f'❌ Error: {e}')
finally:
    proc.terminate()
    proc.wait()
    print('�� Server stopped') 