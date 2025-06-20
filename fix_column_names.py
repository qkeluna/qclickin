#!/usr/bin/env python3
"""
Script to fix camelCase column references to snake_case
"""

import re
import os

def fix_file(filepath):
    """Fix column references in a Python file"""
    if not os.path.exists(filepath):
        print(f"❌ File not found: {filepath}")
        return False
        
    with open(filepath, 'r') as f:
        content = f.read()
    
    original_content = content
    
    # Replace column references
    replacements = {
        # Foreign key columns
        r'\.userId\b': '.user_id',
        r'userId\s*=': 'user_id=',
        r'EventType\.userId': 'EventType.user_id',
        r'Booking\.userId': 'Booking.user_id',
        r'Membership\.userId': 'Membership.user_id',
        r'Webhook\.userId': 'Webhook.user_id',
        
        r'\.teamId\b': '.team_id',
        r'teamId\s*=': 'team_id=',
        r'Membership\.teamId': 'Membership.team_id',
        
        r'\.eventTypeId\b': '.event_type_id',
        r'eventTypeId\s*=': 'event_type_id=',
        r'Booking\.eventTypeId': 'Booking.event_type_id',
        r'booking\.eventTypeId': 'booking.event_type_id',
        
        r'\.bookingId\b': '.booking_id',
        r'bookingId\s*=': 'booking_id=',
        r'Attendee\.bookingId': 'Attendee.booking_id',
        
        r'\.organizationId\b': '.organization_id',
        r'organizationId\s*=': 'organization_id=',
        r'EventType\.organizationId': 'EventType.organization_id',
    }
    
    for pattern, replacement in replacements.items():
        content = re.sub(pattern, replacement, content)
    
    if content != original_content:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"✅ Fixed: {filepath}")
        return True
    else:
        print(f"⚪ No changes: {filepath}")
        return False

def main():
    print("🔧 Fixing camelCase column references...")
    
    files_to_fix = [
        'app/main.py',
        'app/endpoints.py'
    ]
    
    fixed_count = 0
    for file_path in files_to_fix:
        if fix_file(file_path):
            fixed_count += 1
    
    print(f"\n✅ Fixed {fixed_count} files!")
    print("Ready to test the login again!")

if __name__ == "__main__":
    main() 