#!/usr/bin/env python3
"""
Database Migration Script for Production
Run this to initialize database tables in production
"""

import os
from sqlalchemy import create_engine, text
from app.database import Base, DATABASE_URL
from app.models import *  # Import all models

def create_tables():
    """Create all database tables"""
    print("🔗 Connecting to database...")
    print(f"Database URL: {DATABASE_URL}")
    
    try:
        engine = create_engine(DATABASE_URL)
        
        # Test connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Database connection successful!")
        
        # Create all tables
        print("📊 Creating database tables...")
        Base.metadata.create_all(bind=engine)
        print("✅ All tables created successfully!")
        
        # Verify tables exist
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name
            """))
            tables = [row[0] for row in result]
            
        print(f"📋 Created tables: {', '.join(tables)}")
        return True
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def main():
    print("🚀 QClickIn Database Migration")
    print("=" * 40)
    
    if create_tables():
        print("\n✅ Database migration completed successfully!")
        print("Your API should now work properly.")
    else:
        print("\n❌ Database migration failed!")
        print("Check your DATABASE_URL and database connection.")

if __name__ == "__main__":
    main() 