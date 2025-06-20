#!/usr/bin/env python3
"""
QClickIn Setup Script
Automates the initial setup of the FastAPI scheduling platform
"""

import os
import sys
import subprocess
import secrets
from pathlib import Path

def run_command(command, description=""):
    """Run a shell command and handle errors"""
    print(f"🔄 {description}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return None

def create_env_file():
    """Create .env file with secure defaults"""
    env_path = Path(".env")
    if env_path.exists():
        response = input("📄 .env file already exists. Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("📄 Keeping existing .env file")
            return
    
    secret_key = secrets.token_urlsafe(32)
    
    env_content = f"""# QClickIn Environment Configuration
DATABASE_URL=postgresql://username:password@localhost/qclickin_dev
SECRET_KEY={secret_key}
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Optional: Xata Integration
XATA_API_KEY=your_xata_api_key_here
XATA_DATABASE_URL=your_xata_database_url_here
"""
    
    with open(env_path, 'w') as f:
        f.write(env_content)
    
    print("✅ .env file created with secure secret key")
    print("⚠️  Please update DATABASE_URL with your actual database credentials")

def main():
    """Main setup function"""
    print("🚀 QClickIn FastAPI Setup")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version.split()[0]} detected")
    
    # Check if virtual environment is active
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        response = input("⚠️  Virtual environment not detected. Continue anyway? (y/N): ")
        if response.lower() != 'y':
            print("💡 Create virtual environment with: python -m venv venv && source venv/bin/activate")
            sys.exit(1)
    
    # Install dependencies
    if run_command("pip install -r requirements.txt", "Installing Python dependencies"):
        print("📦 All dependencies installed")
    else:
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Create .env file
    create_env_file()
    
    # Initialize Alembic if not already done
    if not Path("alembic/versions").exists():
        run_command("alembic revision --autogenerate -m 'Initial migration'", "Creating initial database migration")
    
    # Run tests to verify setup
    if run_command("python -m pytest tests/ -v", "Running test suite"):
        print("🧪 All tests passed")
    else:
        print("⚠️  Some tests failed - this might be expected if database isn't configured yet")
    
    # Final instructions
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Update DATABASE_URL in .env with your PostgreSQL credentials")
    print("2. Run: alembic upgrade head  # Apply database migrations")
    print("3. Run: uvicorn app.main:app --reload  # Start the development server")
    print("4. Visit: http://localhost:8000/docs  # View API documentation")
    print("\n💡 For production deployment, remember to:")
    print("   - Use a strong SECRET_KEY")
    print("   - Enable HTTPS")
    print("   - Configure proper CORS origins")
    print("   - Set up monitoring and logging")

if __name__ == "__main__":
    main() 