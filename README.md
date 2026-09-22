# Airport API

REST API for managing airports, routes, airplanes, flights, crews, orders, and tickets.

The project is built with Django REST Framework and PostgreSQL. It provides JWT authentication, role-based permissions,
filtering, image upload, Swagger documentation, and Docker support.

## Pull Request link (temporary)
https://github.com/pavliukkk/airport-api/pull/3

## Features

* JWT authentication
* User registration and profile management
* Role-based permissions

    * Regular users can view airport information
    * Regular users can create and delete their own orders
    * Administrators have full CRUD access to airport data
* Airport management
* Route management
* Airplane and airplane type management
* Crew management
* Flight management
* Ticket and order management
* Available ticket calculation
* Airplane image upload
* Filtering by names and related objects
* Swagger / OpenAPI documentation
* PostgreSQL database
* Docker and Docker Compose support
* Automated tests

## Technologies

* Python
* Django
* Django REST Framework
* PostgreSQL
* Simple JWT
* drf-spectacular
* Docker
* Docker Compose
* pytest / Django TestCase

## Main Models

### Airport

Stores airport information:

* name
* closest big city

### Route

Represents a route between two airports:

* source
* destination
* distance

Source and destination airports must be different.

### Airplane Type

Stores airplane types such as:

* Boeing
* Airbus

### Airplane

Stores airplane information:

* name
* rows
* seats per row
* airplane type
* image

The airplane capacity is calculated automatically:

```text
capacity = rows × seats_in_row
```

### Crew

Stores crew members:

* first name
* last name

### Flight

Connects:

* route
* airplane
* crew

and contains:

* departure time
* arrival time

The API also calculates the number of available tickets.

### Order

An order belongs to an authenticated user and contains tickets.

### Ticket

Represents a specific seat on a flight:

* row
* seat
* flight
* order

Each seat can only be booked once for a particular flight.

## Authentication

The API uses JWT authentication.

Users can register and obtain authentication tokens through the authentication endpoints.

Protected endpoints require an access token:

```http
Authorization: Bearer <access_token>
```

## Permissions

The API uses role-based permissions.

### Regular user

A regular authenticated user can:

* view airports
* view routes
* view airplanes
* view airplane types
* view crews
* view flights
* create orders
* view their own orders
* delete their own orders

A regular user cannot modify airport-related data.

### Administrator

An administrator can:

* create objects
* update objects
* partially update objects
* delete objects
* upload airplane images
* manage airport-related data

Regular users can only access their own orders.

## Creating an Order

Example request:

```json
{
  "tickets": [
    {
      "row": 1,
      "seat": 1,
      "flight": 1
    },
    {
      "row": 1,
      "seat": 2,
      "flight": 1
    }
  ]
}
```

The order and its tickets are created inside a database transaction.

## API Documentation

The project uses `drf-spectacular` for OpenAPI documentation.

Swagger UI:

```text
/api/docs/
```

ReDoc:

```text
/api/redoc/
```

OpenAPI schema:

```text
/api/schema/
```

The exact URLs may depend on the project's URL configuration.

## Environment Variables

Sensitive configuration is stored in environment variables.

Example `.env`:

```env
SECRET_KEY=your-secret-key
DEBUG=True

POSTGRES_DB=db_name
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_HOST=host
POSTGRES_PORT=port
```

Do not commit `.env` to the repository.

Add it to `.gitignore`:

```text
.env
```

## Local Installation

Clone the repository:

```bash
git clone <repository-url>
cd airport-api
```

Create a virtual environment:

### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Apply migrations:

```bash
python manage.py migrate
```

Create a superuser:

```bash
python manage.py createsuperuser
```

Run the development server:

```bash
python manage.py runserver
```

The API will be available at:

```text
http://127.0.0.1:8000/
```

## Running with Docker

Build and start the containers:

```bash
docker compose up -d --build
```

Check container status:

```bash
docker compose ps
```

View logs:

```bash
docker compose logs
```

Stop containers:

```bash
docker compose down
```

If the PostgreSQL database needs to be recreated:

```bash
docker compose down -v
docker compose up -d --build
```

> `docker compose down -v` removes Docker volumes, including the PostgreSQL database data.

## Running Tests

Run all tests:

```bash
python manage.py test
```

The test suite covers:

* authentication
* permissions
* CRUD operations
* filtering
* orders
* tickets
* flights
* airplane image upload
* administrator and regular user access

## Django Admin

The Django admin panel is available at:

```text
/admin/
```

Create an administrator with:

```bash
python manage.py createsuperuser
```
