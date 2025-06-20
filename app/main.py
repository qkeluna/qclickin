from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List
from .database import get_db, engine
from .models import *
from .auth import *
from .endpoints import (
    teams_router,
    organizations_router,
    attendees_router,
    availability_router,
    analytics_router,
    webhooks_router,
    advanced_bookings_router
)
import uuid
import os

# Create database tables
try:
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables initialized")
except Exception as e:
    print(f"⚠️ Database initialization warning: {e}")

app = FastAPI(
    title="QClickIn - Scheduling Platform", 
    version="1.0.0",
    description="A Cal.com clone built with FastAPI"
)

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include additional routers
app.include_router(teams_router)
app.include_router(organizations_router)
app.include_router(attendees_router)
app.include_router(availability_router)
app.include_router(analytics_router)
app.include_router(webhooks_router)
app.include_router(advanced_bookings_router)

@app.get("/")
async def root():
    return {"message": "Welcome to QClickIn Scheduling Platform API"}

@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """Comprehensive health check with database connectivity test"""
    try:
        # Test database connection
        db.execute("SELECT 1")
        return {
            "status": "healthy", 
            "service": "qclickin-api",
            "timestamp": datetime.utcnow().isoformat(),
            "database": "connected",
            "version": "1.0.0"
        }
    except Exception as e:
        raise HTTPException(
            status_code=503, 
            detail={
                "status": "unhealthy", 
                "service": "qclickin-api", 
                "error": "Database connection failed",
                "timestamp": datetime.utcnow().isoformat()
            }
        )

# Temporary aliases for leapcell.io health check (fix deployment config!)
@app.get("/kaithhealthcheck")
@app.get("/kaithheathcheck") 
async def health_check_alias():
    """Temporary alias for misspelled health check URLs from leapcell.io"""
    return {"status": "healthy", "service": "qclickin-api", "note": "Fix deployment config to use /health"}

@app.get("/debug")
async def debug_info():
    """Debug endpoint to check production configuration"""
    return {
        "environment": os.getenv("ENVIRONMENT", "not-set"),
        "database_url_set": bool(os.getenv("DATABASE_URL")),
        "secret_key_set": bool(os.getenv("SECRET_KEY")),
        "algorithm": os.getenv("ALGORITHM", "not-set"),
        "python_version": os.sys.version,
        "tables_created": "check logs for initialization message"
    }

# Auth endpoints
@app.post("/auth/register", response_model=UserResponse)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user account"""
    # Check if user exists
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Check username if provided
    if user.username:
        db_username = db.query(User).filter(User.username == user.username).first()
        if db_username:
            raise HTTPException(status_code=400, detail="Username already taken")
    
    # Create user
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        username=user.username,
        name=user.name,
        bio=user.bio,
        timeZone=user.timeZone,
        locale=user.locale,
        theme=user.theme
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Create password record
    db_password = UserPassword(hash=hashed_password, userId=db_user.id)
    db.add(db_password)
    db.commit()
    
    return db_user

@app.post("/auth/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Authenticate user and return access token"""
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not user.passwords:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    if not verify_password(form_data.password, user.passwords.hash):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# User endpoints
@app.get("/users/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """Get current authenticated user"""
    return current_user

@app.patch("/users/me", response_model=UserResponse)
async def update_user_profile(
    user_update: UserBase,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update current user's profile"""
    for field, value in user_update.dict(exclude_unset=True).items():
        setattr(current_user, field, value)
    
    db.commit()
    db.refresh(current_user)
    return current_user

# Event Type endpoints
@app.post("/event-types", response_model=EventTypeResponse)
async def create_event_type(
    event_type: EventTypeCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new event type"""
    # Check if slug is unique for this user
    existing = db.query(EventType).filter(
        EventType.userId == current_user.id,
        EventType.slug == event_type.slug
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Event type slug already exists")
    
    db_event_type = EventType(
        **event_type.dict(),
        userId=current_user.id
    )
    db.add(db_event_type)
    db.commit()
    db.refresh(db_event_type)
    return db_event_type

@app.get("/event-types", response_model=List[EventTypeResponse])
async def get_event_types(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all event types for current user"""
    return db.query(EventType).filter(EventType.userId == current_user.id).all()

@app.get("/event-types/{event_type_id}", response_model=EventTypeResponse)
async def get_event_type(
    event_type_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific event type"""
    event_type = db.query(EventType).filter(
        EventType.id == event_type_id,
        EventType.userId == current_user.id
    ).first()
    if not event_type:
        raise HTTPException(status_code=404, detail="Event type not found")
    return event_type

@app.patch("/event-types/{event_type_id}", response_model=EventTypeResponse)
async def update_event_type(
    event_type_id: int,
    event_type_update: EventTypeBase,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update event type"""
    event_type = db.query(EventType).filter(
        EventType.id == event_type_id,
        EventType.userId == current_user.id
    ).first()
    if not event_type:
        raise HTTPException(status_code=404, detail="Event type not found")
    
    for field, value in event_type_update.dict(exclude_unset=True).items():
        setattr(event_type, field, value)
    
    db.commit()
    db.refresh(event_type)
    return event_type

@app.delete("/event-types/{event_type_id}")
async def delete_event_type(
    event_type_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete event type"""
    event_type = db.query(EventType).filter(
        EventType.id == event_type_id,
        EventType.userId == current_user.id
    ).first()
    if not event_type:
        raise HTTPException(status_code=404, detail="Event type not found")
    
    db.delete(event_type)
    db.commit()
    return {"message": "Event type deleted successfully"}

# Public booking endpoints (no auth required)
@app.get("/public/{username}")
async def get_user_public_profile(username: str, db: Session = Depends(get_db)):
    """Get user's public profile and event types"""
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    event_types = db.query(EventType).filter(
        EventType.userId == user.id,
        EventType.hidden == False
    ).all()
    
    return {
        "user": {
            "name": user.name,
            "bio": user.bio,
            "avatar": user.avatar,
            "theme": user.theme,
            "brandColor": user.brandColor
        },
        "eventTypes": event_types
    }

@app.get("/public/{username}/{event_slug}")
async def get_public_event_type(username: str, event_slug: str, db: Session = Depends(get_db)):
    """Get public event type details"""
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    event_type = db.query(EventType).filter(
        EventType.userId == user.id,
        EventType.slug == event_slug,
        EventType.hidden == False
    ).first()
    if not event_type:
        raise HTTPException(status_code=404, detail="Event type not found")
    
    return event_type

# Booking endpoints
@app.post("/bookings", response_model=BookingResponse)
async def create_booking(
    booking: BookingCreate,
    db: Session = Depends(get_db)
):
    """Create a new booking (public endpoint)"""
    # Check if event type exists
    event_type = db.query(EventType).filter(EventType.id == booking.eventTypeId).first()
    if not event_type:
        raise HTTPException(status_code=404, detail="Event type not found")
    
    # Create booking
    booking_uid = str(uuid.uuid4())
    db_booking = Booking(
        uid=booking_uid,
        userId=event_type.userId,
        eventTypeId=booking.eventTypeId,
        title=booking.title,
        description=booking.description,
        startTime=booking.startTime,
        endTime=booking.endTime,
        location=booking.location
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    
    # Create attendee
    db_attendee = Attendee(
        email=booking.attendeeEmail,
        name=booking.attendeeName,
        timeZone=booking.attendeeTimeZone,
        bookingId=db_booking.id
    )
    db.add(db_attendee)
    db.commit()
    
    return db_booking

@app.get("/bookings", response_model=List[BookingResponse])
async def get_bookings(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all bookings for current user"""
    return db.query(Booking).filter(Booking.userId == current_user.id).all()

@app.get("/bookings/{booking_id}", response_model=BookingResponse)
async def get_booking(
    booking_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific booking"""
    booking = db.query(Booking).filter(
        Booking.id == booking_id,
        Booking.userId == current_user.id
    ).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking

@app.patch("/bookings/{booking_id}")
async def update_booking_status(
    booking_id: int,
    status: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update booking status (accept, reject, cancel)"""
    if status not in ["ACCEPTED", "REJECTED", "CANCELLED"]:
        raise HTTPException(status_code=400, detail="Invalid status")
    
    booking = db.query(Booking).filter(
        Booking.id == booking_id,
        Booking.userId == current_user.id
    ).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    booking.status = status
    db.commit()
    return {"message": f"Booking {status.lower()} successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 