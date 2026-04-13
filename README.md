# UrbanX API
### Unified Smart City & Marketplace Platform

![CI](https://github.com/jessraffelson-del/urbanx-api/actions/workflows/ci.yml/badge.svg)

A production-ready REST and GraphQL API platform built with Django REST Framework, featuring real-time WebSocket notifications, automated testing, and comprehensive documentation.

---

## Features

- **RESTful API** — Full CRUD operations for city services and marketplace products/orders
- **API Versioning** — URI-based versioning (v1, v2) for safe, non-breaking evolution
- **Bulk Operations** — Bulk create support across all endpoints via shared core serializer
- **Standardized Responses** — Consistent response envelope across all endpoints
- **Caching** — Cache-Control headers and ETag conditional requests
- **Rate Limiting** — Throttling with X-RateLimit headers for anonymous and authenticated users
- **WebSockets** — Real-time order and city event notifications via Django Channels
- **GraphQL** — Flexible querying with graphene-django alongside REST endpoints
- **Automated Testing** — 13 tests across city and marketplace apps with pytest
- **CI/CD** — GitHub Actions pipeline runs full test suite on every push
- **Observability** — Structured logging with severity levels across all apps
- **Documentation** — Auto-generated OpenAPI 3.0 / Swagger UI via drf-spectacular

---

## Architecture

urbanx-api/
├── urbanx/          # Project config, settings, URLs, ASGI, GraphQL schema
├── core/            # Shared utilities — base ViewSet, serializers, mixins, responses
├── city/            # City services app — models, views, serializers, consumers, tests
├── marketplace/     # Marketplace app — products, orders, consumers, tests
└── requirements.txt

The project follows a **decoupled architecture** with two domain apps (`city`, `marketplace`) sharing common infrastructure through a `core` app. This separation means changes to one domain can't break the other, and shared behavior (bulk create, response formatting, caching, rate limiting) is defined once and inherited everywhere.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | Django 6.0 + Django REST Framework |
| Real-time | Django Channels + Daphne (ASGI) |
| GraphQL | Graphene-Django |
| Testing | pytest + pytest-django |
| Documentation | drf-spectacular (OpenAPI 3.0) |
| CI/CD | GitHub Actions |

---

## Getting Started

### Prerequisites
- Python 3.14+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/jessraffelson-del/urbanx-api.git
cd urbanx-api

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python3 manage.py migrate

# Start the server
python3 manage.py runserver
```

---

## API Endpoints

### Base URL

http://127.0.0.1:8000/api/v1/

### City Services
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v1/services/` | List all city services |
| POST | `/api/v1/services/` | Create service (single or bulk) |
| GET | `/api/v1/services/{id}/` | Retrieve a service |
| PUT | `/api/v1/services/{id}/` | Update a service |
| DELETE | `/api/v1/services/{id}/` | Delete a service |

### Marketplace
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v1/products/` | List all products |
| POST | `/api/v1/products/` | Create product (single or bulk) |
| GET | `/api/v1/products/available/` | List available products |
| GET | `/api/v1/products/{id}/orders/` | List orders for a product |
| GET | `/api/v1/orders/` | List all orders |
| POST | `/api/v1/orders/` | Create order (single or bulk) |
| POST | `/api/v1/orders/{id}/confirm/` | Confirm an order |

---

## Documentation

| Interface | URL |
|---|---|
| Swagger UI | `/api/docs/` |
| ReDoc | `/api/redoc/` |
| OpenAPI Schema | `/api/schema/` |
| GraphiQL | `/graphql/` |

---

## GraphQL

The GraphQL endpoint supports flexible querying alongside the REST API.

### Example Queries

```graphql
# Get all products with specific fields
{
  allProducts {
    id
    name
    price
    category
  }
}

# Filter by category
{
  productsByCategory(category: "book") {
    name
    price
    stock
  }
}

# Query orders with nested product details
{
  allOrders {
    id
    status
    customerName
    totalPrice
    product {
      name
      category
    }
  }
}
```

---

## WebSockets

Real-time notifications are available via WebSocket connections.

| Endpoint | Description |
|---|---|
| `ws://localhost:8000/ws/city/events/` | City event notifications |
| `ws://localhost:8000/ws/marketplace/orders/` | Order update notifications |

### Example Connection

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/marketplace/orders/');
ws.onmessage = (event) => console.log(JSON.parse(event.data));
```

---

## Running Tests

```bash
# Run full test suite
pytest -v

# Run with coverage report
pytest --cov=city --cov=marketplace --cov=core --cov-report=term-missing
```

---

## API Versioning

Both v1 and v2 are available. Version is specified in the URL:

/api/v1/products/   # Version 1
/api/v2/products/   # Version 2

Invalid versions return `404 Not Found`.

---

## Response Format

All endpoints return a standardized response envelope:

```json
{
    "success": true,
    "message": "Retrieved successfully",
    "data": [...],
    "error": null
}
```

---

## Logging

Structured logs are written to `logs/urbanx.log` with severity levels:

- `INFO` — normal operations (creates, confirmations)
- `WARNING` — concerning events (deletions, invalid state transitions)
- `ERROR` — failures requiring attention