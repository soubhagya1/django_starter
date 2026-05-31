# Django Starter - Product Management API

## Overview

A production-oriented Django REST Framework backend project demonstrating authentication, authorization, background processing, caching, API versioning, testing, Dockerization, and modern backend development practices.

This project was built to showcase backend engineering concepts beyond basic CRUD applications.

---

## Features

### Authentication & Security

* JWT Authentication
* Access Token & Refresh Token
* Refresh Token Rotation
* Refresh Token Blacklisting
* User Registration API
* Login API
* Logout API
* Password Hashing
* API Versioning (`/api/v1/`)
* Rate Limiting / Throttling

---

### Authorization (RBAC)

Role-Based Access Control (RBAC)

#### Roles

* Admin
* User
* Custom Roles

#### Permissions

* Create Product
* View Product
* Update Product
* Delete Product

Permissions are assigned to Roles, and Roles are assigned to Users.

---

### Product Management

* Create Product
* Update Product
* Delete Product
* Product Listing
* Product Search
* Product Filtering
* Pagination
* Image Upload
* Video Upload
* Active/Inactive Products

---

### Category Management

* Category
* SubCategory

Product belongs to a SubCategory.

Category is derived through:

```text
Product
  ↓
SubCategory
  ↓
Category
```

---

### Redis

Used for:

* Caching
* Performance Optimization
* Rate Limiting Support

---

### Celery

Used for asynchronous background processing.

Examples:

* Product Creation Email
* Background Tasks

---

### Celery Beat

Used for scheduled jobs.

Examples:

* Periodic Maintenance Tasks
* Scheduled Reports
* Cleanup Jobs

---

### API Documentation

Swagger / OpenAPI documentation using:

* drf-spectacular

Available at:

```text
/api/schema/swagger-ui/
```

---

### Logging

Structured logging implemented for:

* API Requests
* Product Operations
* Background Tasks
* Error Tracking

---

### Exception Handling

Global exception handling for:

* Validation Errors
* Authentication Errors
* Permission Errors
* Server Errors

---

### Testing

Implemented using:

* Pytest
* pytest-django

Coverage:

```text
83%+
```

Tests include:

* JWT Login
* User Registration
* Invalid Login
* RBAC Authorization
* Product Creation
* Product Listing
* Product Search
* Product Filtering
* Refresh Token Blacklisting

---

## Project Architecture

```text
Client
   │
   ▼
Django REST Framework
   │
   ▼
Views
   │
   ▼
Services
   │
   ▼
Selectors
   │
   ▼
PostgreSQL

Redis
   │
   ├── Caching
   └── Rate Limiting

Celery
   │
   └── Background Tasks

Celery Beat
   │
   └── Scheduled Jobs
```

---

## Tech Stack

### Backend

* Python 3.14
* Django 5
* Django REST Framework

### Database

* PostgreSQL

### Cache

* Redis

### Background Jobs

* Celery
* Celery Beat

### Documentation

* drf-spectacular

### Testing

* Pytest
* pytest-django
* pytest-cov

### Containerization

* Docker
* Docker Compose

---

## API Versioning

All APIs are exposed through:

```text
/api/v1/
```

Examples:

```text
/api/v1/register/
/api/v1/login/
/api/v1/logout/
/api/v1/products/
/api/v1/products/create/
```

---

## RBAC Design

```text
User
  │
  ▼
Role
  │
  ▼
Permission
```

Example:

```text
Admin
 ├── create_product
 ├── update_product
 ├── delete_product
 └── view_product

User
 └── view_product
```

---

## Folder Structure

```text
apps/

├── accounts/
├── products/
├── rbac/

config/

├── settings/
├── urls.py

tests/

Docker

docker-compose.yml
Dockerfile
```

---

## Running Locally

### Build Containers

```bash
docker compose build
```

### Start Services

```bash
docker compose up
```

### Run Migrations

```bash
docker compose exec web python manage.py migrate
```

### Create Superuser

```bash
docker compose exec web python manage.py createsuperuser
```

---

## Running Tests

Run all tests:

```bash
docker compose exec web pytest
```

Run coverage:

```bash
docker compose exec web pytest --cov=apps
```

---

## Future Improvements

* CI/CD with GitHub Actions
* AWS Deployment
* Audit Logs
* Email Templates
* Notification System
* Multi-Tenant Support
* Object Storage (S3)
* Advanced Reporting

---

## Key Backend Concepts Demonstrated

* JWT Authentication
* Refresh Token Rotation
* Refresh Token Blacklisting
* RBAC
* Service Layer Pattern
* Selector Layer Pattern
* Redis Caching
* Celery Background Tasks
* Celery Beat Scheduling
* Dockerized Deployment
* API Versioning
* Structured Logging
* Global Exception Handling
* Automated Testing
* Code Coverage

---

## Author

Backend Engineering Project built to demonstrate production-grade Django REST Framework development practices.
