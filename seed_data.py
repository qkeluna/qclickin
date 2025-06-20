#!/usr/bin/env python3
"""
Seed data script for QClickIn platform
Creates test data for teams, organizations, event types, bookings, attendees, etc.
Excludes users table since test user already exists.
"""

import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import (
    Team, Organization, EventType, Booking, Attendee, 
    Membership, Webhook, User
)

load_dotenv()

# Database connection
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_test_user(db):
    """Get the existing test user"""
    user = db.query(User).filter(User.email == "lunaxcode2030@gmail.com").first()
    if not user:
        print("❌ Test user not found. Please ensure lunaxcode2030@gmail.com exists.")
        return None
    return user

def create_seed_data():
    """Create comprehensive seed data"""
    db = SessionLocal()
    
    try:
        print("🌱 Creating seed data for QClickIn platform...")
        print("=" * 60)
        
        # Get test user
        test_user = get_test_user(db)
        if not test_user:
            return False
        
        print(f"👤 Using test user: {test_user.email} (ID: {test_user.id})")
        
        # 1. Create Organizations
        print("\n🏢 Creating Organizations...")
        organizations = [
            Organization(
                name="TechCorp Inc",
                slug="techcorp",
                org_metadata={"industry": "Technology", "size": "500+"}
            ),
            Organization(
                name="StartupHub",
                slug="startuphub", 
                org_metadata={"industry": "Consulting", "size": "50-100"}
            )
        ]
        
        for org in organizations:
            # Check if already exists
            existing = db.query(Organization).filter(Organization.slug == org.slug).first()
            if not existing:
                db.add(org)
                print(f"   ✅ Created organization: {org.name}")
            else:
                print(f"   ⚪ Organization already exists: {org.name}")
        
        db.commit()
        
        # Get created organizations
        techcorp = db.query(Organization).filter(Organization.slug == "techcorp").first()
        startuphub = db.query(Organization).filter(Organization.slug == "startuphub").first()
        
        # 2. Create Teams
        print("\n👥 Creating Teams...")
        teams = [
            Team(
                name="Engineering Team",
                slug="engineering",
                bio="Software development and technical interviews",
                hideBranding=False,
                team_metadata={"department": "Engineering", "focus": "Backend"}
            ),
            Team(
                name="Sales Team", 
                slug="sales",
                bio="Customer meetings and product demos",
                hideBranding=False,
                team_metadata={"department": "Sales", "focus": "B2B"}
            )
        ]
        
        for team in teams:
            existing = db.query(Team).filter(Team.slug == team.slug).first()
            if not existing:
                db.add(team)
                print(f"   ✅ Created team: {team.name}")
            else:
                print(f"   ⚪ Team already exists: {team.name}")
        
        db.commit()
        
        # Get created teams
        eng_team = db.query(Team).filter(Team.slug == "engineering").first()
        sales_team = db.query(Team).filter(Team.slug == "sales").first()
        
        # 3. Create Memberships
        print("\n🤝 Creating Memberships...")
        memberships = [
            Membership(
                team_id=eng_team.id,
                user_id=test_user.id,
                accepted=True,
                role="OWNER"
            ),
            Membership(
                team_id=sales_team.id,
                user_id=test_user.id,
                accepted=True,
                role="ADMIN"
            )
        ]
        
        for membership in memberships:
            existing = db.query(Membership).filter(
                Membership.team_id == membership.team_id,
                Membership.user_id == membership.user_id
            ).first()
            if not existing:
                db.add(membership)
                print(f"   ✅ Created membership: User {membership.user_id} in Team {membership.team_id}")
            else:
                print(f"   ⚪ Membership already exists")
        
        db.commit()
        
        # 4. Create Event Types
        print("\n📅 Creating Event Types...")
        event_types = [
            EventType(
                title="Technical Interview",
                slug="tech-interview",
                description="45-minute technical interview for software engineering positions",
                length=45,
                hidden=False,
                userId=test_user.id,
                teamId=eng_team.id,
                organizationId=techcorp.id,
                requiresConfirmation=True,
                minimumBookingNotice=1440,  # 24 hours
                price=0,
                currency="usd",
                locations=[{"type": "zoom", "link": "https://zoom.us/j/123456789"}],
                event_metadata={"type": "interview", "level": "senior"}
            ),
            EventType(
                title="Product Demo",
                slug="product-demo",
                description="30-minute product demonstration for potential clients",
                length=30,
                hidden=False,
                userId=test_user.id,
                teamId=sales_team.id,
                organizationId=techcorp.id,
                requiresConfirmation=False,
                minimumBookingNotice=120,  # 2 hours
                price=0,
                currency="usd",
                locations=[{"type": "meet", "link": "https://meet.google.com/abc-defg-hij"}],
                event_metadata={"type": "demo", "audience": "enterprise"}
            ),
            EventType(
                title="Consultation Call",
                slug="consultation",
                description="60-minute strategy consultation",
                length=60,
                hidden=False,
                userId=test_user.id,
                organizationId=startuphub.id,
                requiresConfirmation=True,
                minimumBookingNotice=720,  # 12 hours
                price=15000,  # $150.00
                currency="usd",
                locations=[{"type": "phone", "number": "+1-555-0123"}],
                event_metadata={"type": "consultation", "paid": True}
            )
        ]
        
        for event_type in event_types:
            existing = db.query(EventType).filter(
                EventType.slug == event_type.slug,
                EventType.userId == test_user.id
            ).first()
            if not existing:
                db.add(event_type)
                print(f"   ✅ Created event type: {event_type.title}")
            else:
                print(f"   ⚪ Event type already exists: {event_type.title}")
        
        db.commit()
        
        # Get created event types
        tech_interview = db.query(EventType).filter(EventType.slug == "tech-interview").first()
        product_demo = db.query(EventType).filter(EventType.slug == "product-demo").first()
        consultation = db.query(EventType).filter(EventType.slug == "consultation").first()
        
        # 5. Create Bookings
        print("\n📝 Creating Bookings...")
        now = datetime.utcnow()
        bookings = [
            Booking(
                uid="booking_tech_001",
                userId=test_user.id,
                eventTypeId=tech_interview.id,
                title="Senior Backend Engineer Interview - John Doe",
                description="Technical interview for senior backend position",
                startTime=now + timedelta(days=2, hours=14),  # Day after tomorrow 2 PM
                endTime=now + timedelta(days=2, hours=14, minutes=45),
                location="Zoom Meeting",
                status="ACCEPTED",
                paid=False,
                booking_metadata={"candidate": "John Doe", "position": "Senior Backend Engineer"},
                responses={"experience": "5 years", "stack": "Python, PostgreSQL"}
            ),
            Booking(
                uid="booking_demo_001", 
                userId=test_user.id,
                eventTypeId=product_demo.id,
                title="Product Demo - Acme Corp",
                description="Product demonstration for Acme Corporation",
                startTime=now + timedelta(days=1, hours=10),  # Tomorrow 10 AM
                endTime=now + timedelta(days=1, hours=10, minutes=30),
                location="Google Meet",
                status="ACCEPTED",
                paid=False,
                booking_metadata={"company": "Acme Corp", "attendees": 3},
                responses={"company_size": "500+", "use_case": "internal tools"}
            ),
            Booking(
                uid="booking_consult_001",
                userId=test_user.id,
                eventTypeId=consultation.id,
                title="Strategy Consultation - StartupXYZ",
                description="Business strategy consultation",
                startTime=now + timedelta(days=3, hours=16),  # 3 days from now 4 PM
                endTime=now + timedelta(days=3, hours=17),
                location="Phone Call",
                status="PENDING",
                paid=True,
                booking_metadata={"company": "StartupXYZ", "stage": "Series A"},
                responses={"revenue": "$1M ARR", "team_size": "25"}
            )
        ]
        
        for booking in bookings:
            existing = db.query(Booking).filter(Booking.uid == booking.uid).first()
            if not existing:
                db.add(booking)
                print(f"   ✅ Created booking: {booking.title}")
            else:
                print(f"   ⚪ Booking already exists: {booking.title}")
        
        db.commit()
        
        # Get created bookings
        tech_booking = db.query(Booking).filter(Booking.uid == "booking_tech_001").first()
        demo_booking = db.query(Booking).filter(Booking.uid == "booking_demo_001").first()
        consult_booking = db.query(Booking).filter(Booking.uid == "booking_consult_001").first()
        
        # 6. Create Attendees
        print("\n👨‍💼 Creating Attendees...")
        attendees = [
            Attendee(
                email="john.doe@example.com",
                name="John Doe",
                timeZone="America/New_York",
                locale="en",
                phoneNumber="+1-555-0101",
                bookingId=tech_booking.id,
                noShow=False
            ),
            Attendee(
                email="sarah.johnson@acmecorp.com",
                name="Sarah Johnson",
                timeZone="America/Los_Angeles", 
                locale="en",
                phoneNumber="+1-555-0102",
                bookingId=demo_booking.id,
                noShow=False
            ),
            Attendee(
                email="mike.chen@acmecorp.com",
                name="Mike Chen",
                timeZone="America/Los_Angeles",
                locale="en",
                bookingId=demo_booking.id,
                noShow=False
            ),
            Attendee(
                email="alex.startup@startupxyz.com",
                name="Alex Rodriguez",
                timeZone="America/Chicago",
                locale="en",
                phoneNumber="+1-555-0103",
                bookingId=consult_booking.id,
                noShow=False
            )
        ]
        
        for attendee in attendees:
            existing = db.query(Attendee).filter(
                Attendee.email == attendee.email,
                Attendee.bookingId == attendee.bookingId
            ).first()
            if not existing:
                db.add(attendee)
                print(f"   ✅ Created attendee: {attendee.name} ({attendee.email})")
            else:
                print(f"   ⚪ Attendee already exists: {attendee.name}")
        
        db.commit()
        
        # 7. Create Webhooks
        print("\n🔗 Creating Webhooks...")
        webhooks = [
            Webhook(
                id="wh_slack_notifications",
                subscriber_url="https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX",
                event_triggers=["booking.created", "booking.cancelled", "booking.rescheduled"],
                active=True,
                user_id=test_user.id,
                team_id=eng_team.id
            ),
            Webhook(
                id="wh_crm_integration",
                subscriber_url="https://api.salesforce.com/webhooks/booking-events",
                event_triggers=["booking.created", "booking.completed"],
                active=True,
                user_id=test_user.id,
                team_id=sales_team.id
            )
        ]
        
        for webhook in webhooks:
            existing = db.query(Webhook).filter(Webhook.id == webhook.id).first()
            if not existing:
                db.add(webhook)
                print(f"   ✅ Created webhook: {webhook.id}")
            else:
                print(f"   ⚪ Webhook already exists: {webhook.id}")
        
        db.commit()
        
        print("\n🎉 Seed data creation completed successfully!")
        print("\n📊 Summary:")
        print(f"   🏢 Organizations: {db.query(Organization).count()}")
        print(f"   👥 Teams: {db.query(Team).count()}")
        print(f"   🤝 Memberships: {db.query(Membership).count()}")
        print(f"   📅 Event Types: {db.query(EventType).count()}")
        print(f"   📝 Bookings: {db.query(Booking).count()}")
        print(f"   👨‍💼 Attendees: {db.query(Attendee).count()}")
        print(f"   🔗 Webhooks: {db.query(Webhook).count()}")
        
        print("\n🚀 Ready to test all endpoints with realistic data!")
        return True
        
    except Exception as e:
        print(f"❌ Error creating seed data: {e}")
        db.rollback()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    success = create_seed_data()
    if success:
        print("\n✅ Seed data script completed successfully!")
        print("You can now test all endpoints with rich sample data.")
    else:
        print("\n❌ Seed data script failed!")
        print("Please check the error messages above.") 