from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, and_, or_
from datetime import datetime, timedelta, date
from typing import List, Optional
from .database import get_db
from .models import *
from .auth import get_current_user
import uuid

# Create router instances for different feature groups
teams_router = APIRouter(prefix="/teams", tags=["teams"])
organizations_router = APIRouter(prefix="/organizations", tags=["organizations"])
attendees_router = APIRouter(prefix="/attendees", tags=["attendees"])
availability_router = APIRouter(prefix="/availability", tags=["availability"])
analytics_router = APIRouter(prefix="/analytics", tags=["analytics"])
webhooks_router = APIRouter(prefix="/webhooks", tags=["webhooks"])
advanced_bookings_router = APIRouter(prefix="/bookings", tags=["advanced-bookings"])

# ============================================================================
# TEAM MANAGEMENT ENDPOINTS
# ============================================================================

@teams_router.post("", response_model=TeamResponse, status_code=status.HTTP_201_CREATED)
async def create_team(
    team: TeamCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new team"""
    # Check if slug is unique
    existing = db.query(Team).filter(Team.slug == team.slug).first()
    if existing:
        raise HTTPException(status_code=400, detail="Team slug already exists")
    
    db_team = Team(**team.dict())
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    
    # Create membership for team creator as OWNER
    membership = Membership(
        team_id=db_team.id,
        user_id=current_user.id,
        accepted=True,
        role="OWNER"
    )
    db.add(membership)
    db.commit()
    
    return db_team

@teams_router.get("", response_model=List[TeamResponse])
async def get_user_teams(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get teams user belongs to"""
    teams = db.query(Team).join(Membership).filter(
        Membership.user_id == current_user.id,
        Membership.accepted == True
    ).all()
    return teams

@teams_router.get("/{team_id}", response_model=TeamResponse)
async def get_team(
    team_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific team"""
    team = db.query(Team).join(Membership).filter(
        Team.id == team_id,
        Membership.user_id == current_user.id,
        Membership.accepted == True
    ).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team

@teams_router.patch("/{team_id}", response_model=TeamResponse)
async def update_team(
    team_id: int,
    team_update: TeamBase,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update team details (requires ADMIN or OWNER role)"""
    # Check permission
    membership = db.query(Membership).filter(
        Membership.team_id == team_id,
        Membership.user_id == current_user.id,
        Membership.role.in_(["ADMIN", "OWNER"]),
        Membership.accepted == True
    ).first()
    if not membership:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    for field, value in team_update.dict(exclude_unset=True).items():
        setattr(team, field, value)
    
    db.commit()
    db.refresh(team)
    return team

@teams_router.delete("/{team_id}")
async def delete_team(
    team_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete team (requires OWNER role)"""
    membership = db.query(Membership).filter(
        Membership.team_id == team_id,
        Membership.user_id == current_user.id,
        Membership.role == "OWNER",
        Membership.accepted == True
    ).first()
    if not membership:
        raise HTTPException(status_code=403, detail="Only team owners can delete teams")
    
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    db.delete(team)
    db.commit()
    return {"message": "Team deleted successfully"}

# Team Membership Endpoints
@teams_router.post("/{team_id}/members", response_model=MembershipResponse, status_code=status.HTTP_201_CREATED)
async def invite_team_member(
    team_id: int,
    invite: MembershipInvite,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Invite member to team"""
    # Check permission
    membership = db.query(Membership).filter(
        Membership.team_id == team_id,
        Membership.user_id == current_user.id,
        Membership.role.in_(["ADMIN", "OWNER"]),
        Membership.accepted == True
    ).first()
    if not membership:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    # Find user by email
    user = db.query(User).filter(User.email == invite.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if already member
    existing = db.query(Membership).filter(
        Membership.team_id == team_id,
        Membership.user_id == user.id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="User is already a team member")
    
    new_membership = Membership(
        team_id=team_id,
        user_id=user.id,
        role=invite.role,
        accepted=False  # Requires acceptance
    )
    db.add(new_membership)
    db.commit()
    db.refresh(new_membership)
    
    return new_membership

@teams_router.get("/{team_id}/members", response_model=List[MembershipResponse])
async def get_team_members(
    team_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get team members"""
    # Check if user is team member
    membership = db.query(Membership).filter(
        Membership.team_id == team_id,
        Membership.user_id == current_user.id,
        Membership.accepted == True
    ).first()
    if not membership:
        raise HTTPException(status_code=403, detail="Access denied")
    
    members = db.query(Membership).options(joinedload(Membership.user)).filter(
        Membership.team_id == team_id,
        Membership.accepted == True
    ).all()
    return members

@teams_router.patch("/{team_id}/members/{user_id}", response_model=MembershipResponse)
async def update_member_role(
    team_id: int,
    user_id: int,
    role_update: MembershipBase,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update member role"""
    # Check permission
    current_membership = db.query(Membership).filter(
        Membership.team_id == team_id,
        Membership.user_id == current_user.id,
        Membership.role.in_(["ADMIN", "OWNER"]),
        Membership.accepted == True
    ).first()
    if not current_membership:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    target_membership = db.query(Membership).filter(
        Membership.team_id == team_id,
        Membership.user_id == user_id
    ).first()
    if not target_membership:
        raise HTTPException(status_code=404, detail="Membership not found")
    
    target_membership.role = role_update.role
    db.commit()
    db.refresh(target_membership)
    return target_membership

@teams_router.delete("/{team_id}/members/{user_id}")
async def remove_team_member(
    team_id: int,
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Remove team member"""
    # Check permission (ADMIN/OWNER can remove others, users can leave themselves)
    if user_id != current_user.id:
        current_membership = db.query(Membership).filter(
            Membership.team_id == team_id,
            Membership.user_id == current_user.id,
            Membership.role.in_(["ADMIN", "OWNER"]),
            Membership.accepted == True
        ).first()
        if not current_membership:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    membership = db.query(Membership).filter(
        Membership.team_id == team_id,
        Membership.user_id == user_id
    ).first()
    if not membership:
        raise HTTPException(status_code=404, detail="Membership not found")
    
    db.delete(membership)
    db.commit()
    return {"message": "Member removed successfully"}

# ============================================================================
# ORGANIZATION MANAGEMENT ENDPOINTS
# ============================================================================

@organizations_router.post("", response_model=OrganizationResponse, status_code=status.HTTP_201_CREATED)
async def create_organization(
    org: OrganizationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new organization"""
    existing = db.query(Organization).filter(Organization.slug == org.slug).first()
    if existing:
        raise HTTPException(status_code=400, detail="Organization slug already exists")
    
    db_org = Organization(**org.dict())
    db.add(db_org)
    db.commit()
    db.refresh(db_org)
    return db_org

@organizations_router.get("", response_model=List[OrganizationResponse])
async def get_organizations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's organizations"""
    # This would typically be filtered by user permissions
    orgs = db.query(Organization).all()
    return orgs

# ============================================================================
# ATTENDEE MANAGEMENT ENDPOINTS
# ============================================================================

@attendees_router.get("/bookings/{booking_id}/attendees", response_model=List[AttendeeResponse])
async def get_booking_attendees(
    booking_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get booking attendees"""
    booking = db.query(Booking).filter(
        Booking.id == booking_id,
        Booking.user_id == current_user.id
    ).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    attendees = db.query(Attendee).filter(Attendee.booking_id == booking_id).all()
    return attendees

@attendees_router.patch("/{attendee_id}", response_model=AttendeeResponse)
async def update_attendee(
    attendee_id: int,
    attendee_update: AttendeeUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update attendee information"""
    attendee = db.query(Attendee).join(Booking).filter(
        Attendee.id == attendee_id,
        Booking.user_id == current_user.id
    ).first()
    if not attendee:
        raise HTTPException(status_code=404, detail="Attendee not found")
    
    for field, value in attendee_update.dict(exclude_unset=True).items():
        setattr(attendee, field, value)
    
    db.commit()
    db.refresh(attendee)
    return attendee

@attendees_router.patch("/{attendee_id}/no-show")
async def mark_attendee_no_show(
    attendee_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mark attendee as no-show"""
    attendee = db.query(Attendee).join(Booking).filter(
        Attendee.id == attendee_id,
        Booking.user_id == current_user.id
    ).first()
    if not attendee:
        raise HTTPException(status_code=404, detail="Attendee not found")
    
    attendee.noShow = True
    db.commit()
    return {"message": "Attendee marked as no-show"}

# ============================================================================
# AVAILABILITY MANAGEMENT ENDPOINTS
# ============================================================================

@availability_router.get("/users/{user_id}/availability")
async def get_user_availability(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get user availability (public endpoint)"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "timeZone": user.timeZone,
        "startTime": user.startTime,
        "endTime": user.endTime,
        "bufferTime": user.bufferTime,
        "weekStart": user.weekStart
    }

@availability_router.patch("/users/me/availability")
async def update_user_availability(
    availability: AvailabilityUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user availability"""
    for field, value in availability.dict(exclude_unset=True).items():
        setattr(current_user, field, value)
    
    db.commit()
    db.refresh(current_user)
    return {"message": "Availability updated successfully"}

@availability_router.get("/public/{username}/{event_slug}/slots", response_model=List[TimeSlot])
async def get_available_slots(
    username: str,
    event_slug: str,
    date: date = Query(..., description="Date to get slots for (YYYY-MM-DD)"),
    timezone: str = Query("UTC", description="Timezone for the slots"),
    db: Session = Depends(get_db)
):
    """Get available time slots for booking"""
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    event_type = db.query(EventType).filter(
        EventType.user_id == user.id,
        EventType.slug == event_slug,
        EventType.hidden == False
    ).first()
    if not event_type:
        raise HTTPException(status_code=404, detail="Event type not found")
    
    # Get existing bookings for the date
    start_of_day = datetime.combine(date, datetime.min.time())
    end_of_day = datetime.combine(date, datetime.max.time())
    
    existing_bookings = db.query(Booking).filter(
        Booking.user_id == user.id,
        Booking.startTime >= start_of_day,
        Booking.endTime <= end_of_day,
        Booking.status == "ACCEPTED"
    ).all()
    
    # Generate available slots (simplified logic)
    slots = []
    current_time = start_of_day.replace(
        hour=user.startTime // 60,
        minute=user.startTime % 60
    )
    end_time = start_of_day.replace(
        hour=user.endTime // 60,
        minute=user.endTime % 60
    )
    
    while current_time + timedelta(minutes=event_type.length) <= end_time:
        slot_end = current_time + timedelta(minutes=event_type.length)
        
        # Check if slot conflicts with existing bookings
        is_available = True
        for booking in existing_bookings:
            if (current_time < booking.endTime and slot_end > booking.startTime):
                is_available = False
                break
        
        slots.append(TimeSlot(
            start=current_time,
            end=slot_end,
            available=is_available
        ))
        
        current_time += timedelta(minutes=30)  # 30-minute intervals
    
    return slots

# ============================================================================
# ADVANCED BOOKING ENDPOINTS
# ============================================================================

@advanced_bookings_router.post("/{booking_id}/reschedule")
async def reschedule_booking(
    booking_id: int,
    reschedule_data: BookingReschedule,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Reschedule a booking"""
    booking = db.query(Booking).filter(
        Booking.id == booking_id,
        Booking.user_id == current_user.id
    ).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    booking.startTime = reschedule_data.startTime
    booking.endTime = reschedule_data.endTime
    db.commit()
    
    return {"message": "Booking rescheduled successfully"}

@advanced_bookings_router.post("/{booking_id}/cancel")
async def cancel_booking(
    booking_id: int,
    cancel_data: BookingCancel,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Cancel a booking"""
    booking = db.query(Booking).filter(
        Booking.id == booking_id,
        Booking.user_id == current_user.id
    ).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    booking.status = "CANCELLED"
    db.commit()
    
    return {"message": "Booking cancelled successfully"}

@advanced_bookings_router.get("/{booking_id}/full", response_model=BookingWithAttendees)
async def get_booking_with_attendees(
    booking_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get booking with all attendee details"""
    booking = db.query(Booking).options(joinedload(Booking.attendees)).filter(
        Booking.id == booking_id,
        Booking.user_id == current_user.id
    ).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    return booking

# ============================================================================
# ANALYTICS ENDPOINTS
# ============================================================================

@analytics_router.get("/bookings", response_model=BookingAnalytics)
async def get_booking_analytics(
    start_date: date = Query(...),
    end_date: date = Query(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get booking analytics for date range"""
    start_datetime = datetime.combine(start_date, datetime.min.time())
    end_datetime = datetime.combine(end_date, datetime.max.time())
    
    bookings = db.query(Booking).filter(
        Booking.user_id == current_user.id,
        Booking.startTime >= start_datetime,
        Booking.startTime <= end_datetime
    ).all()
    
    total_bookings = len(bookings)
    confirmed_bookings = len([b for b in bookings if b.status == "ACCEPTED"])
    cancelled_bookings = len([b for b in bookings if b.status == "CANCELLED"])
    pending_bookings = len([b for b in bookings if b.status == "PENDING"])
    
    # Calculate revenue (simplified)
    revenue = sum(
        db.query(EventType).filter(EventType.id == booking.event_type_id).first().price / 100
        for booking in bookings if booking.status == "ACCEPTED"
    )
    
    return BookingAnalytics(
        total_bookings=total_bookings,
        confirmed_bookings=confirmed_bookings,
        cancelled_bookings=cancelled_bookings,
        pending_bookings=pending_bookings,
        revenue=revenue,
        period_start=start_datetime,
        period_end=end_datetime
    )

@analytics_router.get("/event-types", response_model=List[EventTypePerformance])
async def get_event_type_performance(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get event type performance metrics"""
    event_types = db.query(EventType).filter(EventType.user_id == current_user.id).all()
    performance_data = []
    
    for event_type in event_types:
        bookings = db.query(Booking).filter(Booking.event_type_id == event_type.id).all()
        total_bookings = len(bookings)
        confirmed_bookings = len([b for b in bookings if b.status == "ACCEPTED"])
        
        performance_data.append(EventTypePerformance(
            event_type_id=event_type.id,
            title=event_type.title,
            total_bookings=total_bookings,
            conversion_rate=confirmed_bookings / total_bookings if total_bookings > 0 else 0,
            average_duration=event_type.length,
            revenue=confirmed_bookings * event_type.price / 100
        ))
    
    return performance_data

# ============================================================================
# WEBHOOK ENDPOINTS
# ============================================================================

@webhooks_router.post("", response_model=WebhookResponse, status_code=status.HTTP_201_CREATED)
async def create_webhook(
    webhook: WebhookCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new webhook"""
    db_webhook = Webhook(
        **webhook.dict(),
        user_id=current_user.id
    )
    db.add(db_webhook)
    db.commit()
    db.refresh(db_webhook)
    return db_webhook

@webhooks_router.get("", response_model=List[WebhookResponse])
async def get_webhooks(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user webhooks"""
    webhooks = db.query(Webhook).filter(Webhook.user_id == current_user.id).all()
    return webhooks

@webhooks_router.delete("/{webhook_id}")
async def delete_webhook(
    webhook_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a webhook"""
    webhook = db.query(Webhook).filter(
        Webhook.id == webhook_id,
        Webhook.user_id == current_user.id
    ).first()
    if not webhook:
        raise HTTPException(status_code=404, detail="Webhook not found")
    
    db.delete(webhook)
    db.commit()
    return {"message": "Webhook deleted successfully"}