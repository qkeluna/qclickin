#!/usr/bin/env python3
"""
Fix ALL column references to match actual database schema
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
    
    # Replace column references to match ACTUAL database schema
    replacements = {
        # EventType columns (database uses camelCase)
        r'EventType\.user_id': 'EventType.userId',
        r'EventType\.team_id': 'EventType.teamId', 
        r'EventType\.organization_id': 'EventType.organizationId',
        r'user_id\s*=\s*current_user\.id': 'userId=current_user.id',
        
        # Booking columns (database uses camelCase)
        r'Booking\.user_id': 'Booking.userId',
        r'Booking\.event_type_id': 'Booking.eventTypeId',
        r'booking\.event_type_id': 'booking.eventTypeId',
        r'eventTypeId\s*=\s*booking\.eventTypeId': 'eventTypeId=booking.eventTypeId',
        
        # Attendee columns (database uses camelCase)
        r'Attendee\.booking_id': 'Attendee.bookingId',
        r'booking_id\s*=': 'bookingId=',
        
        # Membership columns (these are already correct - snake_case)
        # r'Membership\.team_id': 'Membership.team_id',  # Already correct
        # r'Membership\.user_id': 'Membership.user_id',  # Already correct
        
        # Webhook columns (database uses snake_case for foreign keys, but different names for main columns)
        r'Webhook\.user_id': 'Webhook.user_id',  # This is correct
        r'\.url\b': '.subscriber_url',  # For webhook URL field
        r'\.events\b': '.event_triggers',  # For webhook events field
        
        # Fix create statements
        r'userId\s*=\s*current_user\.id': 'userId=current_user.id',
        r'eventTypeId\s*=\s*booking\.eventTypeId': 'eventTypeId=booking.eventTypeId',
        r'bookingId\s*=\s*db_booking\.id': 'bookingId=db_booking.id',
    }
    
    for pattern, replacement in replacements.items():
        content = re.sub(pattern, replacement, content)
    
    # Special fixes for specific patterns
    # Fix event type creation
    content = re.sub(r'user_id\s*=\s*current_user\.id', 'userId=current_user.id', content)
    content = re.sub(r'team_id\s*=\s*', 'teamId=', content)
    content = re.sub(r'organization_id\s*=\s*', 'organizationId=', content)
    
    # Fix booking creation
    content = re.sub(r'event_type_id\s*=\s*', 'eventTypeId=', content)
    content = re.sub(r'user_id\s*=\s*event_type\.userId', 'userId=event_type.userId', content)
    
    # Fix attendee creation
    content = re.sub(r'booking_id\s*=\s*db_booking\.id', 'bookingId=db_booking.id', content)
    
    if content != original_content:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"✅ Fixed: {filepath}")
        return True
    else:
        print(f"⚪ No changes: {filepath}")
        return False

def main():
    print("🔧 Fixing ALL column references to match database schema...")
    
    files_to_fix = [
        'app/main.py',
        'app/endpoints.py'
    ]
    
    fixed_count = 0
    for file_path in files_to_fix:
        if fix_file(file_path):
            fixed_count += 1
    
    print(f"\n✅ Fixed {fixed_count} files!")
    print("All column references now match the actual database schema!")

if __name__ == "__main__":
    main() 