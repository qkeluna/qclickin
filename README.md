# QClickIn - Scheduling Platform API

A FastAPI-based scheduling platform inspired by Cal.com, built with modern Python technologies and following Test-Driven Development (TDD) principles.

## 🎯 Features

- **User Management**: Registration, authentication, and profile management
- **Event Types**: Create and manage different types of scheduling events
- **Booking System**: Public booking interface and booking management
- **Team & Organization Support**: Multi-tenant architecture
- **REST API**: Comprehensive API with automatic documentation
- **Database Migrations**: Alembic integration for schema management
- **Testing**: Comprehensive test suite with pytest
- **Authentication**: JWT-based authentication with bcrypt password hashing

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- PostgreSQL database
- Virtual environment (recommended)

### Installation

1. **Clone and navigate to the project**:

   ```bash
   cd qclickin
   ```

2. **Create and activate virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Copy the environment template and update with your values:

   ```bash
   cp env.template .env
   # Edit .env with your actual database URL and generate a secure SECRET_KEY
   ```

   **🔒 Security Note**: Never commit your `.env` file! It's already in `.gitignore`.

5. **Initialize database migrations**:

   ```bash
   alembic revision --autogenerate -m "Initial migration"
   alembic upgrade head
   ```

6. **Run the application**:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

### Interactive Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Core Endpoints

#### Authentication

- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user (returns JWT token)

#### User Management

- `GET /users/me` - Get current user profile
- `PATCH /users/me` - Update user profile

#### Event Types

- `POST /event-types` - Create event type
- `GET /event-types` - List user's event types
- `GET /event-types/{id}` - Get specific event type
- `PATCH /event-types/{id}` - Update event type
- `DELETE /event-types/{id}` - Delete event type

#### Public Booking

- `GET /public/{username}` - Get user's public profile and events
- `GET /public/{username}/{event_slug}` - Get specific event details
- `POST /bookings` - Create a booking (public endpoint)

#### Booking Management

- `GET /bookings` - List user's bookings
- `GET /bookings/{id}` - Get specific booking
- `PATCH /bookings/{id}` - Update booking status

## 🧪 Testing

Run the test suite:

```bash
pytest tests/ -v
```

Run tests with coverage:

```bash
pytest tests/ --cov=app --cov-report=html
```

## 🗄️ Database Management

### Create Migration

```bash
alembic revision --autogenerate -m "Description of changes"
```

### Apply Migrations

```bash
alembic upgrade head
```

### Rollback Migration

```bash
alembic downgrade -1
```

## 🏗️ Project Structure

```
qclickin/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application and routes
│   ├── models.py        # SQLAlchemy & Pydantic models
│   ├── database.py      # Database configuration
│   └── auth.py          # Authentication utilities
├── tests/
│   ├── __init__.py
│   └── test_auth.py     # Authentication tests
├── alembic/
│   ├── env.py           # Alembic environment
│   └── script.py.mako   # Migration template
├── docs/
│   └── fastapi_models_setup.py  # Reference implementation
├── requirements.txt     # Python dependencies
├── alembic.ini         # Alembic configuration
└── README.md           # This file
```

## 📊 Database Schema

### Core Tables

- **users**: User accounts and profiles
- **user_passwords**: Encrypted password storage
- **event_types**: Different types of events users can create
- **bookings**: Scheduled appointments
- **attendees**: People attending bookings
- **teams**: Team/organization support
- **memberships**: User-team relationships

## 🔐 Security Features

- **Password Hashing**: Bcrypt for secure password storage
- **JWT Authentication**: Stateless authentication tokens
- **Input Validation**: Pydantic models for request validation
- **CORS Support**: Configurable cross-origin requests
- **SQL Injection Protection**: SQLAlchemy ORM prevents SQL injection

## 🚀 Development Workflow (Kaizen-AI)

This project follows the ALIVE framework for continuous improvement:

### A - AI-Enhanced Development Loops

1. **RED**: Write failing tests first
2. **GREEN**: Generate minimal passing implementation
3. **REFACTOR**: Improve code quality
4. **AI-INTEGRATE**: Learn and optimize

### Example Development Session:

```bash
# 1. Write a failing test
pytest tests/test_new_feature.py::test_should_fail -v

# 2. Implement minimal solution
# Edit app/main.py to make test pass

# 3. Refactor and improve
# Review code quality, add documentation

# 4. Run full test suite
pytest -v
```

## 🎯 API Usage Examples

### Register User

```bash
curl -X POST "http://localhost:8000/auth/register" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "user@example.com",
       "password": "securepassword",
       "name": "John Doe",
       "username": "johndoe"
     }'
```

### Login

```bash
curl -X POST "http://localhost:8000/auth/login" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=user@example.com&password=securepassword"
```

### Create Event Type

```bash
curl -X POST "http://localhost:8000/event-types" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "30min Meeting",
       "slug": "30min-meeting",
       "description": "Quick 30 minute meeting",
       "length": 30
     }'
```

## 🤝 Contributing

1. Follow TDD principles - write tests first
2. Use descriptive commit messages
3. Ensure all tests pass before submitting PR
4. Update documentation for API changes

## 📝 License

This project is licensed under the MIT License.

## 🔧 Configuration

### Environment Variables

- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: JWT signing secret (use strong random string in production)
- `ALGORITHM`: JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time (default: 30)

### Production Deployment

1. Set strong `SECRET_KEY`
2. Use production PostgreSQL database
3. Enable HTTPS
4. Configure proper CORS origins
5. Set up monitoring and logging

## 📈 Performance Considerations

- Database indexes on frequently queried fields
- JWT token expiration management
- Connection pooling for database
- Caching strategies for public endpoints
- API rate limiting (to be implemented)

## 🐛 Troubleshooting

### Common Issues

1. **Database connection errors**: Check DATABASE_URL in .env
2. **Migration failures**: Ensure database is running and accessible
3. **Import errors**: Activate virtual environment and install dependencies
4. **Test failures**: Check test database configuration

### Development Tips

- Use `uvicorn app.main:app --reload` for hot reloading during development
- Check logs for detailed error information
- Use the interactive API docs at /docs for testing endpoints
