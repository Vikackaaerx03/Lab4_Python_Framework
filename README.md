# Laboratory Work No. 4

## Project Title
Order REST API

## Individual Assignment
Variant 11

Entity: `Order`

Fields:
- `id` - unique identifier
- `order_number` - order number
- `customer_name` - customer name
- `total_price` - total amount
- `order_date` - order date

## Laboratory Task
Tasks for Laboratory Work No. 4:

1. Create a REST API according to the individual assignment.
2. Implement at least 2 HTTP methods (`GET` and `POST`).
3. Return data in JSON format.
4. Test the API in a browser or Postman.

## Implemented Solution
This project is based on Laboratory Work No. 3 and reuses the same `Order` entity and SQLite database approach.

The new part added for Lab 4 is a REST API built with:
- `FastAPI`
- `SQLite`
- `SQLAlchemy`
- `Jinja2`
- `Uvicorn`

## API Features
- Web interface for browser testing
- Get all orders
- Get one order by ID
- Create a new order
- Update an order
- Delete an order
- Return responses in JSON format
- Validate incoming data
- Store data in SQLite database

## Validation Rules
- `order_number` must contain exactly 3 digits in format `001`
- `order_number` must be the next available sequential number
- `customer_name` cannot be empty
- `total_price` must be greater than `0`
- `order_date` cannot be in the future

Example:
- If existing numbers are `001`, `002`, `003`, the next valid number is `004`

## Project Structure
```text
Lab4_Python_Framework/
  app/
    main.py
    database.py
    models.py
    schemas.py
    crud.py
    router/
      order.py
      web.py
    templates/
      index.html
      create.html
      edit.html
    static/
      style.css
  orders.db
  pyproject.toml
  README.md
```

## Website Pages
- `/` - main orders page
- `/create` - create order form
- `/edit/{order_id}` - edit order form
- `/delete/{order_id}` - delete order from browser

## Endpoints
### `GET /api/orders/`
Returns all orders in JSON format.

Example response:
```json
[
  {
    "id": 1,
    "order_number": "001",
    "customer_name": "Anna",
    "total_price": 1200.5,
    "order_date": "2026-03-31"
  }
]
```

### `GET /api/orders/{order_id}`
Returns one order by its ID.

### `POST /api/orders/`
Creates a new order.

Example request body:
```json
{
  "order_number": "001",
  "customer_name": "Anna Ivanenko",
  "total_price": 1200.5,
  "order_date": "2026-03-31"
}
```

Example response:
```json
{
  "id": 1,
  "order_number": "001",
  "customer_name": "Anna Ivanenko",
  "total_price": 1200.5,
  "order_date": "2026-03-31"
}
```

### `GET /api/orders/meta/next-number`
Returns the next valid order number.

Example response:
```json
{
  "next_order_number": "004"
}
```

### `PUT /api/orders/{order_id}`
Updates an existing order.

### `DELETE /api/orders/{order_id}`
Deletes an order by ID.

## How to Run
Install dependencies:

```bash
pip install fastapi uvicorn sqlalchemy jinja2 python-multipart
```

Run the API:

```bash
uvicorn app.main:app --reload
```

Open in browser:

```text
http://127.0.0.1:8000
```

Website pages:

```text
http://127.0.0.1:8000/
http://127.0.0.1:8000/create
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

## Testing
The API can be tested in:
- browser for `GET` requests
- Swagger UI at `/docs`
- Postman for `GET` and `POST` requests

## Result
The developed project implements a REST API for the `Order` entity according to the individual assignment. It supports `GET` and `POST` methods, returns JSON responses, uses SQLite for data storage, and can be tested through the browser, Swagger UI, or Postman.
