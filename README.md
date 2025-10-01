# VaultTecInventory
Flask API , React inventory management system

# VaultTec Inventory — FastAPI + SQLite (ULID/UUID IDs)

Inventory Management System with Clean Architecture vibes, FastAPI, and SQLite using **string IDs** (`TEXT PRIMARY KEY`) generated as UUID/ULID. Tested with `pytest`, managed with `poetry`.

---

## Table of Contents
- [Prerequisites](#prerequisites)
- [Quickstart (Poetry)](#quickstart-poetry)
- [Environment Variables](#environment-variables)
- [Run the API](#run-the-api)
- [Auth — Get a JWT](#auth--get-a-jwt)
- [Products API (CRUD)](#products-api-crud)
- [Run Tests & Coverage](#run-tests--coverage)
- [Coverage Config (.coveragerc)](#coverage-config-coveragerc)
- [Project Structure](#project-structure)
- [Architecture Overview](#architecture-overview)

---

## Prerequisites
- Python 3.11+
- [Poetry](https://python-poetry.org/) 1.6+ (recommended)

---

## Quickstart (Poetry)

```bash
# 1) Install Poetry if needed
curl -sSL https://install.python-poetry.org | python3 -

# 2) Install dependencies
poetry install

# 3) Activate virtualenv
poetry shell
```
If you prefer not to use poetry shell, prefix commands with poetry run ....


## Environment Variables

Create a `.env` or export the following before running:

```bash
export SQLITE_PATH="./infrastructure.db"   # SQLite file path (optional; defaults to ./infrastructure.db)
export JWT_SECRET="change-me"              # REQUIRED: secret to sign JWTs
export JWT_ALG="HS256"                     # optional, default HS256
export JWT_EXPIRES_MIN="60"                # optional, default 60

# For /auth/token convenience during local dev:
export DEV_USER="test"
export DEV_PASS="test"
```

## Run the API
```bash
# Using poetry
poetry run uvicorn inventory.interfaces.http.api:app --reload --port 8000

# Or if you entered `poetry shell` earlier:
uvicorn inventory.interfaces.http.api:app --reload --port 8000
```

## Open Swagger UI: http://localhost:8000/docs

## Auth — Get a JWT
All product endpoints are protected by Bearer JWT. First, obtain a token.

```bash
curl -X POST "http://localhost:8000/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=${DEV_USER:-test}&password=${DEV_PASS:-test}"

## for testing purposes

  TOKEN="$(curl -s -X POST http://localhost:8000/auth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=${DEV_USER:-test}&password=${DEV_PASS:-test}" \
  | python -c 'import sys,json; print(json.load(sys.stdin)["access_token"])')"
echo "TOKEN=$TOKEN"


```


## Products API (CRUD)
```bash

# Create
curl -X POST "http://localhost:8000/products" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Laptop",
    "description": "Lightweight developer machine",
    "price": 1200.50,
    "quantity": 5
  }'
# list
curl -X GET "http://localhost:8000/products" \
  -H "Authorization: Bearer $TOKEN"

curl -X GET "http://localhost:8000/products?q=Laptop" \
  -H "Authorization: Bearer $TOKEN"


  # update
  curl -X PUT "http://localhost:8000/products/PUT_ID_HERE" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Laptop Pro",
    "description": "Upgraded dev machine",
    "price": 1500.75,
    "quantity": 3
  }'

  ```

  ## Run Tests & Coverage
  
  poetry run pytest -q

## Architecture Overview

High-level: Clean-ish layering with a slim interface layer, use-cases in application, pure domain entities, and replaceable infra.

      +-------------------+
      |   HTTP (FastAPI)  |  -->  auth.py, router.py, schemas
      +---------+---------+
                |
                v
      +-------------------+
      |   Application     |  -->  product_* use cases (no framework deps)
      +---------+---------+
                |
                v
      +-------------------+
      |     Domain        |  -->  entities.Product (id: str, value fields)
      +---------+---------+
                |
                v
      +-------------------+
      |  Infrastructure   |  -->  SQLite UoW + Repo (TEXT PRIMARY KEY)
      +-------------------+


 🚀