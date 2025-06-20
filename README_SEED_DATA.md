# 🌱 Seed Data for QClickIn Platform

This document describes the seed data created for testing all endpoints in the QClickIn booking platform.

## Overview

The `seed_data.py` script creates comprehensive test data for all non-user tables, providing realistic scenarios for testing all API endpoints.

## What Gets Created

### 🏢 Organizations (2 records)

- **TechCorp Inc** - Technology company (500+ employees)
- **StartupHub** - Consulting company (50-100 employees)

### 👥 Teams (2 records)

- **Engineering Team** - Software development and technical interviews
- **Sales Team** - Customer meetings and product demos

### 🤝 Memberships (2 records)

- Test user as OWNER of Engineering Team
- Test user as ADMIN of Sales Team

### 📅 Event Types (3 records)

- **Technical Interview** (45 min) - For engineering team, requires confirmation
- **Product Demo** (30 min) - For sales team, no confirmation needed
- **Consultation Call** (60 min) - Paid consultation ($150), requires confirmation

### 📝 Bookings (3 records)

- **Senior Backend Engineer Interview** - Scheduled 2 days from now
- **Product Demo - Acme Corp** - Scheduled tomorrow
- **Strategy Consultation - StartupXYZ** - Scheduled 3 days from now (PENDING, paid)

### 👨‍💼 Attendees (4 records)

- **John Doe** - Technical interview candidate
- **Sarah Johnson & Mike Chen** - Acme Corp demo attendees
- **Alex Rodriguez** - StartupXYZ consultation client

### 🔗 Webhooks (2 records)

- **Slack Notifications** - For engineering team booking events
- **CRM Integration** - For sales team booking events

## Usage

### Running the Seed Script

```bash
python seed_data.py
```

The script will:

- ✅ Check for existing test user (lunaxcode2030@gmail.com)
- ✅ Create all seed data with duplicate prevention
- ✅ Show detailed progress with emojis
- ✅ Provide summary statistics

### Expected Output

```
🌱 Creating seed data for QClickIn platform...
============================================================
👤 Using test user: lunaxcode2030@gmail.com (ID: 34)

🏢 Creating Organizations...
   ✅ Created organization: TechCorp Inc
   ✅ Created organization: StartupHub

👥 Creating Teams...
   ✅ Created team: Engineering Team
   ✅ Created team: Sales Team

🤝 Creating Memberships...
   ✅ Created membership: User 34 in Team 1
   ✅ Created membership: User 34 in Team 2

📅 Creating Event Types...
   ✅ Created event type: Technical Interview
   ✅ Created event type: Product Demo
   ✅ Created event type: Consultation Call

📝 Creating Bookings...
   ✅ Created booking: Senior Backend Engineer Interview - John Doe
   ✅ Created booking: Product Demo - Acme Corp
   ✅ Created booking: Strategy Consultation - StartupXYZ

👨‍💼 Creating Attendees...
   ✅ Created attendee: John Doe (john.doe@example.com)
   ✅ Created attendee: Sarah Johnson (sarah.johnson@acmecorp.com)
   ✅ Created attendee: Mike Chen (mike.chen@acmecorp.com)
   ✅ Created attendee: Alex Rodriguez (alex.startup@startupxyz.com)

🔗 Creating Webhooks...
   ✅ Created webhook: wh_slack_notifications
   ✅ Created webhook: wh_crm_integration

🎉 Seed data creation completed successfully!

📊 Summary:
   🏢 Organizations: 2
   👥 Teams: 2
   🤝 Memberships: 2
   📅 Event Types: 3
   📝 Bookings: 3
   👨‍💼 Attendees: 4
   🔗 Webhooks: 2

🚀 Ready to test all endpoints with realistic data!
```

## Testing Endpoints

With this seed data, you can now test:

### ✅ Working Endpoints

- `/event-types` - List and create event types
- `/bookings` - List user bookings
- `/teams` - List user teams
- `/organizations` - List and create organizations
- `/webhooks` - List webhooks
- `/users/me` - Get current user profile
- `/public/{username}` - Public user profiles

### 🔧 Endpoints Needing Parameters

- `/analytics/bookings?start_date=2024-01-01&end_date=2024-12-31`
- `/availability?date=2024-01-15&eventTypeId=1`

### 📊 Rich Test Data Features

- **Realistic Names & Emails** - Professional-looking test data
- **Time Zones** - Multiple time zones for attendees
- **Metadata** - Rich JSON metadata for all entities
- **Relationships** - Proper foreign key relationships
- **Status Variety** - Different booking statuses (ACCEPTED, PENDING)
- **Payment Scenarios** - Both free and paid event types

## Database Schema Alignment

The seed data is created using the corrected SQLAlchemy models that align with the actual PostgreSQL database schema:

- Uses `userId`, `teamId`, `organizationId` (camelCase) for foreign keys
- Proper `metadata` column mapping for teams and organizations
- Correct webhook field names (`subscriber_url`, `event_triggers`)

## Prerequisites

- Existing test user: `lunaxcode2030@gmail.com`
- Database connection configured in `.env`
- All SQLAlchemy models properly aligned with database schema

## Safety Features

- **Duplicate Prevention** - Checks for existing records before creating
- **Rollback on Error** - Database transaction rollback if any step fails
- **Progress Reporting** - Clear feedback on what's being created
- **Re-runnable** - Safe to run multiple times without duplicating data

---

🎯 **Ready to test all your endpoints with realistic, comprehensive data!**
