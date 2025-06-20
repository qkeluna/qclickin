#!/usr/bin/env python3
"""
Environment Setup Script for QClickIn
Helps create .env file and test database connection
"""

import os
import secrets
from pathlib import Path

def create_env_file():
    """Create .env file with database configuration"""
    env_file = Path(".env")
    
    if env_file.exists():
        print("📄 .env file already exists!")
        response = input("Do you want to overwrite it? (y/N): ")
        if response.lower() != 'y':
            print("Keeping existing .env file")
            return
    
    print("🔧 Setting up environment variables...")
    
    # Get database URL
    print("\n🗄️  Database Configuration:")
    print("1. Use Xata database (from your docs)")
    print("2. Use SQLite (for local development)")
    print("3. Use PostgreSQL (local)")
    print("4. Custom URL")
    
    choice = input("Select database option (1-4) [default: 1]: ").strip() or "1"
    
    if choice == "1":
        # Xata configuration from your docs
        database_url = "https://Khyle-Erick-Luna-s-workspace-8g1h14.us-east-1.xata.sh/db/qclickin-db:main"
        xata_api_key = "xau_KQgFhYNVwXuFLtPiryNdbmuQPYvQApTV6"
    elif choice == "2":
        database_url = "sqlite:///./qclickin.db"
        xata_api_key = ""
    elif choice == "3":
        database_url = input("Enter PostgreSQL URL (e.g., postgresql://user:pass@localhost/dbname): ")
        xata_api_key = ""
    else:
        database_url = input("Enter your database URL: ")
        xata_api_key = input("Enter Xata API key (if applicable): ")
    
    # Generate secure secret key
    secret_key = secrets.token_urlsafe(32)
    
    # Create .env content
    env_content = f"""# QClickIn Environment Configuration
DATABASE_URL={database_url}
SECRET_KEY={secret_key}
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30"""
    
    if xata_api_key:
        env_content += f"""

# Xata Configuration
XATA_API_KEY={xata_api_key}
XATA_DATABASE_URL={database_url}"""
    
    # Write .env file
    with open(env_file, "w") as f:
        f.write(env_content)
    
    print(f"✅ .env file created successfully!")
    print(f"🔐 Generated secure SECRET_KEY")
    print(f"🗄️  Database URL: {database_url}")

def test_database_connection():
    """Test database connection"""
    print("\n🧪 Testing database connection...")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        from app.database import engine, DATABASE_URL
        
        print(f"🔗 Connecting to: {DATABASE_URL}")
        
        # Test connection
        with engine.connect() as connection:
            result = connection.execute("SELECT 1")
            print("✅ Database connection successful!")
            
    except ImportError as e:
        print(f"⚠️  Import error: {e}")
        print("💡 Make sure to install dependencies first: pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("💡 Check your DATABASE_URL in .env file")

def main():
    print("🚀 QClickIn Environment Setup")
    print("=" * 40)
    
    # Create .env file
    create_env_file()
    
    # Test connection
    if input("\n🧪 Test database connection? (Y/n): ").lower() != 'n':
        test_database_connection()
    
    print("\n" + "=" * 40)
    print("✅ Environment setup complete!")
    print("\n📋 Next steps:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Run migrations: alembic upgrade head")
    print("3. Start server: uvicorn app.main:app --reload")
    print("4. Visit: http://localhost:8000/docs")

if __name__ == "__main__":
    main() 