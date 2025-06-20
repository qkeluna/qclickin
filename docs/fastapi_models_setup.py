# FastAPI Models & Database Setup for Cal.com Clone
# Run this after fixing your database schema naming

# requirements.txt
"""
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
python-multipart==0.0.6
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-dotenv==1.0.0
pydantic[email]==2.5.0
alembic==1.13.0
httpx==0.25.2
"""

# .env
"""
XATA_API_KEY=xau_KQgFhYNVwXuFLtPiryNdbmuQPYvQApTV6
XATA_DATABASE_URL=https://Khyle-Erick-Luna-s-workspace-8g1h14.us-east-1.xata.sh/db/qclickin-db:main
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
"""

# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# app/models.py
from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field

# SQLAlchemy Models (Database)
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True)
    name = Column(String)
    bio = Column(Text)
    avatar = Column(Text)
    timeZone = Column(String, default="UTC")
    weekStart = Column(String, default="Sunday")
    startTime = Column(Integer, default=0)  # Minutes from midnight
    endTime = Column(Integer, default=1440)  # Minutes from midnight
    bufferTime = Column(Integer, default=0)
    locale = Column(String, default="en")
    theme = Column(String, default="light")
    emailVerified = Column(DateTime)
    identityProvider = Column(String, default="CAL")
    identityProviderId = Column(String)
    twoFactorEnabled = Column(Boolean, default=False)
    twoFactorSecret = Column(String)
    role = Column(String, default="USER")
    plan = Column(String, default="FREE")
    brandColor = Column(String, default="#292929")
    darkBrandColor = Column(String, default="#fafafa")
    hideBranding = Column(Boolean, default=False)
    allowDynamicBooking = Column(Boolean, default=True)
    metadata = Column(JSONB, default={})
    completedOnboarding = Column(Boolean, default=False)
    createdDate = Column(DateTime, default=func.now())
    
    # Relationships
    passwords = relationship("UserPassword", back_populates="user", uselist=False)
    event_types = relationship("EventType", back_populates="user")
    bookings = relationship("Booking", back_populates="user")
    memberships = relationship("Membership", back_populates="user")

class UserPassword(Base):
    __tablename__ = "user_passwords"
    
    id = Column(Integer, primary_key=True, index=True)
    hash = Column(String, nullable=False)
    userId = Column(Integer, ForeignKey("users.id"), unique=True)
    
    # Relationships
    user = relationship("User", back_populates="passwords")

class EventType(Base):
    __tablename__ = "event_types"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    slug = Column(String, nullable=False)
    description = Column(Text)
    position = Column(Integer, default=0)
    length = Column(Integer, nullable=False)  # Duration in minutes
    offsetStart = Column(Integer, default=0)
    hidden = Column(Boolean, default=False)
    userId = Column(Integer, ForeignKey("users.id"))
    teamId = Column(Integer, ForeignKey("teams.id"))
    organizationId = Column(Integer, ForeignKey("organizations.id"))
    requiresConfirmation = Column(Boolean, default=False)
    disableGuests = Column(Boolean, default=False)
    minimumBookingNotice = Column(Integer, default=120)  # Minutes
    beforeEventBuffer = Column(Integer, default=0)
    afterEventBuffer = Column(Integer, default=0)
    seatsPerTimeSlot = Column(Integer)
    schedulingType = Column(String)  # ROUND_ROBIN, COLLECTIVE, MANAGED
    periodType = Column(String, default="UNLIMITED")
    locations = Column(JSONB, default=[])
    metadata = Column(JSONB, default={})
    price = Column(Integer, default=0)  # Price in cents
    currency = Column(String, default="usd")
    
    # Relationships
    user = relationship("User", back_populates="event_types")
    bookings = relationship("Booking", back_populates="event_type")

class Booking(Base):
    __tablename__ = "bookings"
    
    id = Column(Integer, primary_key=True, index=True)
    uid = Column(String, unique=True, nullable=False)
    userId = Column(Integer, ForeignKey("users.id"))
    eventTypeId = Column(Integer, ForeignKey("event_types.id"))
    title = Column(String, nullable=False)
    description = Column(Text)
    startTime = Column(DateTime, nullable=False)
    endTime = Column(DateTime, nullable=False)
    location = Column(Text)
    status = Column(String, default="ACCEPTED")  # CANCELLED, ACCEPTED, REJECTED, PENDING
    paid = Column(Boolean, default=False)
    metadata = Column(JSONB, default={})
    responses = Column(JSONB, default={})
    
    # Relationships
    user = relationship("User", back_populates="bookings")
    event_type = relationship("EventType", back_populates="bookings")
    attendees = relationship("Attendee", back_populates="booking")

class Attendee(Base):
    __tablename__ = "attendees"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False)
    name = Column(String, nullable=False)
    timeZone = Column(String, default="UTC")
    locale = Column(String, default="en")
    phoneNumber = Column(String)
    bookingId = Column(Integer, ForeignKey("bookings.id"))
    noShow = Column(Boolean, default=False)
    
    # Relationships
    booking = relationship("Booking", back_populates="attendees")

# Pydantic Models (API)
class UserBase(BaseModel):
    email: EmailStr
    username: Optional[str] = None
    name: Optional[str] = None
    bio: Optional[str] = None
    timeZone: str = "UTC"
    locale: str = "en"
    theme: str = "light"

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    role: str
    plan: str
    completedOnboarding: bool
    createdDate: datetime
    
    class Config:
        from_attributes = True

class EventTypeBase(BaseModel):
    title: str
    slug: str
    description: Optional[str] = None
    length: int  # Duration in minutes
    hidden: bool = False
    requiresConfirmation: bool = False
    minimumBookingNotice: int = 120
    price: int = 0
    currency: str = "usd"

class EventTypeCreate(EventTypeBase):
    pass

class EventTypeResponse(EventTypeBase):
    id: int
    userId: int
    position: int
    
    class Config:
        from_attributes = True

class BookingBase(BaseModel):
    title: str
    description: Optional[str] = None
    startTime: datetime
    endTime: datetime
    location: Optional[str] = None

class BookingCreate(BookingBase):
    eventTypeId: int
    attendeeEmail: EmailStr
    attendeeName: str
    attendeeTimeZone: str = "UTC"

class BookingResponse(BookingBase):
    id: int
    uid: str
    userId: int
    eventTypeId: int
    status: str
    
    class Config:
        from_attributes = True

class AttendeeResponse(BaseModel):
    id: int
    email: str
    name: str
    timeZone: str
    noShow: bool
    
    class Config:
        from_attributes = True

# app/auth.py
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .database import get_db
from .models import User
import os

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.email == username).first()
    if user is None:
        raise credentials_exception
    return user

# app/main.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import timedelta
from .database import get_db
from .models import *
from .auth import *
import uuid

app = FastAPI(title="Cal.com Clone API", version="1.0.0")

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Auth endpoints
@app.post("/auth/register", response_model=UserResponse)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user exists
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
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
    return current_user

# Event Type endpoints
@app.post("/event-types", response_model=EventTypeResponse)
async def create_event_type(
    event_type: EventTypeCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
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
    return db.query(EventType).filter(EventType.userId == current_user.id).all()

# Booking endpoints
@app.post("/bookings", response_model=BookingResponse)
async def create_booking(
    booking: BookingCreate,
    db: Session = Depends(get_db)
):
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
    return db.query(Booking).filter(Booking.userId == current_user.id).all()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)