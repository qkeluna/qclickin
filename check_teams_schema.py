#!/usr/bin/env python3
"""
Check teams table schema specifically
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

def check_teams_schema():
    """Check teams table columns"""
    print("🔍 Teams Table Schema:")
    print("=" * 30)
    
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns 
            WHERE table_name = 'teams'
            ORDER BY ordinal_position
        """))
        
        columns = result.fetchall()
        
        for col in columns:
            nullable = "NULL" if col[2] == "YES" else "NOT NULL"
            default = f" DEFAULT {col[3]}" if col[3] else ""
            print(f"   {col[0]}: {col[1]} {nullable}{default}")

if __name__ == "__main__":
    check_teams_schema() 