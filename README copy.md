# Django Enterprise Starter

A production-oriented Django REST Framework backend project built to learn enterprise application architecture and backend development concepts.

## Features

### Authentication

- Custom User Model
- Registration
- Login / Logout
- JWT Authentication
- Access Token
- Refresh Token

### Role Based Access Control (RBAC)

- Roles
- Permissions
- Role Permission Mapping
- User Role Mapping
- Custom DRF Permission Classes

### Product Management

- Categories
- Sub Categories
- Products
- Manufacturing Details
- Owner Details

### API Features

- Django REST Framework
- Class Based APIs
- Serializers
- Pagination
- Search
- Filtering
- Validation

### Architecture

- Service Layer Pattern
- Selector Layer Pattern
- Separation of Business Logic
- Reusable Components

### Database

- PostgreSQL
- Django ORM
- Migrations

### Caching

- Redis
- Product List Caching

### Background Tasks

- Celery
- Async Email Tasks

### Scheduling

- Celery Beat
- Periodic Tasks

### Security

- JWT Authentication
- Role Based Authorization
- API Throttling / Rate Limiting

### Deployment

- Docker
- Docker Compose
- WhiteNoise Static File Handling

---

## Project Structure

```text
apps/
├── accounts/
├── products/
├── rbac/

config/
├── settings/
│   ├── base.py
│   ├── dev.py
│   └── prod.py
├── celery.py
├── urls.py
```

## Tech Stack

- Python 3.13+
- Django 5
- Django REST Framework
- PostgreSQL
- Redis
- Celery
- Celery Beat
- Docker
- WhiteNoise

## Implemented Concepts

- Custom User Model
- JWT Authentication
- RBAC
- Service Layer
- Selector Layer
- DRF APIs
- Pagination
- Filtering
- Search
- Redis Caching
- Celery Tasks
- Celery Beat Scheduling
- Rate Limiting
- Dockerized Deployment

## Future Enhancements

- Email Verification
- Password Reset
- OTP Authentication
- Swagger/OpenAPI
- Audit Logs
- Soft Deletes
- CI/CD Pipeline
- AWS Deployment



HTML Pages(Traditional Django)-
/register/
/login/
/logout/
/admin/

API side(Django REST Framework)-
/Products/
/api/token/
/api/token/refresh/

Product API(class ProductListAPIView(APIView)) not Product HTML Page(class ProductListView(ListView)
)

Current User Flow
Admin-
Admin Login
 ↓
Admin Panel
 ↓
Create Category
 ↓
Create Subcategory
 ↓
Create Role
 ↓
Create Permission
 ↓
Assign Role

Normal User- Currently normal users do NOT have a dashboard.
Register
 ↓
Login
 ↓
Use APIs

Project Goal-
A backend-focused Django application demonstrating enterprise architecture patterns.

1. Django Web Authentication
/register/
/login/
/logout/
/admin/

uses-
SessionAuthentication
CSRF Protection
Cookies

2. API Authentication
/api/token/
/api/token/refresh/
/products/

uses-
JWT
Authorization: Bearer xxx
No CSRF required.

API Documentation
1. Register User
POST /api/register/
2. Assign permission to user to see /products 

if role and permission  table empth then seed them or create all permission and roles from admin

to seed permissions
docker-compose exec web python manage.py seed_permission

then from admin create roles and assign permissions to it then access /products


✓ JWT Authentication
✓ JWT Refresh
✓ Refresh Token Rotation
✓ Refresh Token Blacklisting
✓ RBAC (Role + Permission)
✓ Product APIs
✓ Search & Filtering
✓ Pagination
✓ Redis Caching
✓ Celery Tasks
✓ Celery Beat
✓ Rate Limiting
✓ Swagger/OpenAPI
✓ Global Exception Handling
✓ Structured Logging
✓ Docker
✓ Pytest
✓ 83% Coverage
✓ API Versioning (/api/v1/)
✓ Automated Security Tests
✓ Service Layer
✓ Selector Layer

The biggest thing missing now is presentation and documentation, not another technical feature.
focus -
README.md
Architecture Diagram
API Documentation
Interview Notes

Many mid-level backend candidates won't have all of these in one project.

README should contain:
Project Overview

Architecture

Features

Tech Stack

Project Structure

Installation

Docker Setup

API Endpoints

Swagger

Testing

Coverage

Future Improvements

Architecture Diagram-
Client
  ↓
DRF API
  ↓
Views
  ↓
Services
  ↓
Selectors
  ↓
PostgreSQL

Redis
  ↓
Cache

Celery
  ↓
Background Tasks

API Documentation-
POST /api/v1/register/
POST /api/v1/login/
POST /api/v1/logout/

GET /api/v1/products/
POST /api/v1/products/create
PUT /api/v1/products/{id}
DELETE /api/v1/products/{id}

Include:
Request
Response
Auth required?
Permission required?

Create Interview Notes-
INTERVIEW_NOTES.md-
Why Redis?
Why Celery?
Why Service Layer?
Why Selectors?
Why JWT?
Why Refresh Token Blacklist?
Why Docker?
Why API Versioning?
Why RBAC?

dont add-
Sentry
Prometheus
GraphQL
Microservices
Kafka
WebSockets
Those increase complexity but won't help much for a mid-level Python/Django interview.

prioritize:
Finish and document this Django project.
Push it to GitHub with a strong README.
Practice Python interview questions.
Learn Django internals well enough to explain your project.
Continue your FastAPI roadmap (since many newer Python backend jobs use FastAPI).
If you can confidently discuss this project end-to-end and solve typical backend interview questions, you're in a much stronger position than someone who only knows basic Django CRUD

dontdo
Kafka
Microservices
GraphQL
Prometheus
OpenTelemetry
Kubernetes
Sentry
WebSockets

Those won't improve your interview outcome nearly as much as polishing and presenting what you've already built