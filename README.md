# energyar

# Ordering System API

A role-based ordering system built with **Django** and **Django REST Framework (DRF)**. This project provides a RESTful API for managing orders with authentication, role-based permissions, API documentation, and containerized deployment.

## Features

* **Role-based user system**

  * **Customers**

    * Create orders
    * View and manage only their own orders
  * **Managers**

    * Access and manage all orders in the system

* **REST API**

  * Built using **Django REST Framework (DRF)**

* **API Documentation**

  * Integrated **Swagger UI** for easy API exploration and testing

* **Database**

  * Uses **PostgreSQL** for reliable and scalable data storage

* **Containerized Deployment**

  * Dockerized setup using **Docker Compose**

* **API Tests**

  * Includes API tests to ensure system reliability and correctness

---

## Tech Stack

* Python
* Django
* Django REST Framework (DRF)
* PostgreSQL
* Docker & Docker Compose
* Swagger / OpenAPI

---

## User Roles

### Customer

Customers can:

* Create new orders
* View their own orders
* Update or manage their own orders

### Manager

Managers can:

* View all orders
* Manage all customer orders
* Perform administrative order operations

---

## API Documentation

Swagger documentation is available after running the project.

You can access it at:

```bash
http://localhost:8000/api/docs/
```

---

## Running the Project with Docker

This project uses **Docker Compose** for easy setup and deployment.

### Prerequisites

Make sure you have installed:

* Docker
* Docker Compose

### Run the Application

Clone the repository and run:

```bash
docker-compose up --build
```

### Services

After running the containers:

* **Web Application:** `http://localhost:8000`
* **PostgreSQL Database:** runs on port `5432`

To stop the containers:

```bash
docker-compose down
```

---

## Running Tests

API tests are included in this project.

To run the tests:

```bash
docker-compose exec web python manage.py test
```

Or if running locally without Docker:

```bash
python manage.py test
```

---

## Project Status

This project is currently in its **first version (v1)** and will continue to be improved in future releases.

Planned features include:

* Cart system
* Payment integration
* More advanced order management
* Additional improvements and optimizations

Stay tuned for upcoming updates 🚀
