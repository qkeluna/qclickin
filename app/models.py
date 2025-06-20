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
    user_metadata = Column("metadata", JSONB, default={})
    completedOnboarding = Column(Boolean, default=False)
    createdDate = Column(DateTime, default=func.now())
    
    # Relationships
    passwords = relationship("UserPassword", back_populates="user", uselist=False)
    event_types = relationship("EventType", back_populates="user")
    bookings = relationship("Booking", back_populates="user")
    memberships = relationship("Membership", back_populates="user")
    webhooks = relationship("Webhook", back_populates="user")

class UserPassword(Base):
    __tablename__ = "user_passwords"
    
    id = Column(Integer, primary_key=True, index=True)
    hash = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    
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
    user_id = Column(Integer, ForeignKey("users.id"))
    team_id = Column(Integer, ForeignKey("teams.id", ondelete="CASCADE"))
    organization_id = Column(Integer, ForeignKey("organizations.id", ondelete="CASCADE"))
    requiresConfirmation = Column(Boolean, default=False)
    disableGuests = Column(Boolean, default=False)
    minimumBookingNotice = Column(Integer, default=120)  # Minutes
    beforeEventBuffer = Column(Integer, default=0)
    afterEventBuffer = Column(Integer, default=0)
    seatsPerTimeSlot = Column(Integer)
    schedulingType = Column(String)  # ROUND_ROBIN, COLLECTIVE, MANAGED
    periodType = Column(String, default="UNLIMITED")
    locations = Column(JSONB, default=[])
    event_metadata = Column("metadata", JSONB, default={})
    price = Column(Integer, default=0)  # Price in cents
    currency = Column(String, default="usd")
    
    # Relationships
    user = relationship("User", back_populates="event_types")
    bookings = relationship("Booking", back_populates="event_type")

class Booking(Base):
    __tablename__ = "bookings"
    
    id = Column(Integer, primary_key=True, index=True)
    uid = Column(String, unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    event_type_id = Column(Integer, ForeignKey("event_types.id"))
    title = Column(String, nullable=False)
    description = Column(Text)
    startTime = Column(DateTime, nullable=False)
    endTime = Column(DateTime, nullable=False)
    location = Column(Text)
    status = Column(String, default="ACCEPTED")  # CANCELLED, ACCEPTED, REJECTED, PENDING
    paid = Column(Boolean, default=False)
    booking_metadata = Column("metadata", JSONB, default={})
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
    booking_id = Column(Integer, ForeignKey("bookings.id"))
    noShow = Column(Boolean, default=False)
    
    # Relationships
    booking = relationship("Booking", back_populates="attendees")

class Team(Base):
    __tablename__ = "teams"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    slug = Column(String, unique=True, nullable=False)
    logo = Column(String)
    bio = Column(Text)
    hideBranding = Column(Boolean, default=False)
    team_metadata = Column(JSONB, default={})
    createdDate = Column(DateTime, default=func.now())

class Organization(Base):
    __tablename__ = "organizations"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    slug = Column(String, unique=True, nullable=False)
    org_metadata = Column(JSONB, default={})
    createdDate = Column(DateTime, default=func.now())

class Membership(Base):
    __tablename__ = "memberships"
    
    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    accepted = Column(Boolean, default=False)
    role = Column(String, default="MEMBER")  # MEMBER, ADMIN, OWNER
    
    # Relationships
    user = relationship("User", back_populates="memberships")

class Webhook(Base):
    __tablename__ = "webhooks"
    
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)
    events = Column(JSONB, nullable=False)  # List of event types
    active = Column(Boolean, default=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="webhooks")

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
    user_id: int
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
    event_type_id: int
    attendeeEmail: EmailStr
    attendeeName: str
    attendeeTimeZone: str = "UTC"

class BookingResponse(BookingBase):
    id: int
    uid: str
    user_id: int
    event_type_id: int
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

# Team Management Models
class TeamBase(BaseModel):
    name: str
    slug: str
    bio: Optional[str] = None
    hideBranding: bool = False

class TeamCreate(TeamBase):
    pass

class TeamResponse(TeamBase):
    id: int
    createdDate: datetime
    
    class Config:
        from_attributes = True

# Organization Models
class OrganizationBase(BaseModel):
    name: str
    slug: str

class OrganizationCreate(OrganizationBase):
    pass

class OrganizationResponse(OrganizationBase):
    id: int
    createdDate: datetime
    
    class Config:
        from_attributes = True

# Membership Models
class MembershipBase(BaseModel):
    role: str = "MEMBER"  # MEMBER, ADMIN, OWNER

class MembershipInvite(BaseModel):
    email: EmailStr
    role: str = "MEMBER"

class MembershipResponse(BaseModel):
    id: int
    team_id: int
    user_id: int
    accepted: bool
    role: str
    user: Optional[UserResponse] = None
    
    class Config:
        from_attributes = True

# Attendee Management Models
class AttendeeUpdate(BaseModel):
    name: Optional[str] = None
    phoneNumber: Optional[str] = None
    timeZone: Optional[str] = None

# Extended Booking Models
class BookingWithAttendees(BookingResponse):
    attendees: List[AttendeeResponse] = []
    
    class Config:
        from_attributes = True

class BookingReschedule(BaseModel):
    startTime: datetime
    endTime: datetime
    reason: Optional[str] = None

class BookingCancel(BaseModel):
    reason: Optional[str] = None

# Availability Models
class AvailabilityUpdate(BaseModel):
    startTime: Optional[int] = None  # Minutes from midnight
    endTime: Optional[int] = None    # Minutes from midnight
    bufferTime: Optional[int] = None
    timeZone: Optional[str] = None

class TimeSlot(BaseModel):
    start: datetime
    end: datetime
    available: bool = True

# Analytics Models
class BookingAnalytics(BaseModel):
    total_bookings: int
    confirmed_bookings: int
    cancelled_bookings: int
    pending_bookings: int
    revenue: float
    period_start: datetime
    period_end: datetime

class EventTypePerformance(BaseModel):
    event_type_id: int
    title: str
    total_bookings: int
    conversion_rate: float
    average_duration: int
    revenue: float

# Webhook Models
class WebhookBase(BaseModel):
    url: str
    events: List[str]  # booking.created, booking.cancelled, etc.
    active: bool = True

class WebhookCreate(WebhookBase):
    pass

class WebhookResponse(WebhookBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True 