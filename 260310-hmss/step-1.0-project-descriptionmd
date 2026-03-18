# Step 1.0: Context Diagram Blueprint — Hostel Management and Search System

## Problem Description

The Hostel Management and Search System (HMSS) is a web application that enables visitors to search and view hostel room listings, tenants to submit and manage rental requests, property owners to manage properties and room listings, and system administrators to oversee platform operations including owner verification and content moderation. The context diagram below illustrates the external entities and system interfaces.

## Major Features

FE-01: Search hostel room listings using filters (location, price, amenities, availability, move-in date)
FE-02: View detailed room listing information with property and map data
FE-03: Register a Tenant or Owner account
FE-04: Sign in with role-based access control
FE-05: Submit rental request for a room listing
FE-06: Cancel a pending rental request
FE-07: Track rental request statuses
FE-08: Create and update property records
FE-09: Create room listings with image upload (draft status)
FE-10: Update room listing information
FE-11: Publish room listing (verified owners only)
FE-12: Change listing visibility (hide/archive)
FE-13: Submit owner verification documents
FE-14: Review and decide on rental requests (accept/reject)
FE-15: Reopen locked room after failed arrangement
FE-16: Review owner verification submissions (admin)
FE-17: Manage user account status (admin)
FE-18: Control listing visibility for policy violations (admin)

### System Under Consideration

- Hostel Management and Search System (HMSS)

### External Entities

- Visitor
- Tenant
- Owner
- System Admin
- Google Maps
- Cloud Storage
- Email Provider

### Exchanges to Draw

Visitor <-> HMSS

- To system: search criteria, listing selection, registration information
- From system: search results, room details, registration outcome

Tenant <-> HMSS

- To system: sign-in credentials, rental request submission, cancellation request, status inquiry
- From system: authentication result, request status, request outcome

Owner <-> HMSS

- To system: sign-in credentials, property data, room listing data, owner verification submission, request decisions, reopen request
- From system: authentication result, publication result, request lists and request details, verification status, listing state result

System Admin <-> HMSS

- To system: sign-in credentials, verification review decision, account-status change, listing-control action
- From system: verification data, user and listing data, review result, control result

Google Maps <-> HMSS

- To system: map data, geolocation data
- From system: location lookup request

Cloud Storage <-> HMSS

- To system: stored asset reference, retrieved file data
- From system: image upload request, document upload request, asset retrieval request

Email Provider <-> HMSS

- To system: delivery status
- From system: notification dispatch request

### Drawing Notes

1. Draw HMSS as one central black-box system.
2. Place human entities on the left side of the system.
3. Place external service systems on the right side of the system.
4. Keep data-flow labels business-visible and short.
5. Do not show use cases, classes, packages, or internal subsystems in this diagram.
