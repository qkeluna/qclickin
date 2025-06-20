#!/usr/bin/env python3
"""
Check actual database schema vs our models
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

# Database connection
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

def check_table_schema(table_name):
    """Check actual columns in a table"""
    print(f"\n🔍 Checking table: {table_name}")
    print("=" * 40)
    
    with engine.connect() as conn:
        # Get all columns for the table
        result = conn.execute(text("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns 
            WHERE table_name = :table_name
            ORDER BY ordinal_position
        """), {"table_name": table_name})
        
        columns = result.fetchall()
        
        if not columns:
            print(f"❌ Table '{table_name}' not found!")
            return False
        
        print(f"✅ Found {len(columns)} columns:")
        for col in columns:
            nullable = "NULL" if col[2] == "YES" else "NOT NULL"
            default = f" DEFAULT {col[3]}" if col[3] else ""
            print(f"   {col[0]}: {col[1]} {nullable}{default}")
        
        return True

def main():
    print("🔍 Checking Database Schema")
    print("=" * 50)
    
    # Check all main tables
    tables = [
        "users",
        "user_passwords", 
        "event_types",
        "bookings",
        "attendees",
        "teams",
        "organizations",
        "memberships",
        "webhooks"
    ]
    
    for table in tables:
        try:
            check_table_schema(table)
        except Exception as e:
            print(f"❌ Error checking {table}: {e}")
    
    print("\n🔧 Schema Analysis Complete!")

if __name__ == "__main__":
    main() 