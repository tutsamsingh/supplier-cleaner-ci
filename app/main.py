"""
A small FastAPI app that cleans supplier records and saves them to Postgres.

Endpoints:
  GET  /health     -> check the app is running
  POST /clean      -> clean one record and return it (no database)
  POST /suppliers  -> clean one record and save it to the database
  GET  /suppliers  -> list all saved records
"""

import os
from contextlib import asynccontextmanager
from typing import Optional

import psycopg
from fastapi import FastAPI
from pydantic import BaseModel

from app.cleaner import clean_record

# The database address comes from an environment variable.
# docker-compose and the GitHub Actions workflow both set this.
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://app:app@localhost:5432/suppliers"
)


def get_connection():
    """Open a new connection to Postgres."""
    return psycopg.connect(DATABASE_URL)


def create_table():
    """Create the suppliers table if it doesn't exist yet."""
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS suppliers (
                id    SERIAL PRIMARY KEY,
                name  TEXT,
                email TEXT,
                price NUMERIC,
                date  DATE
            )
            """
        )


@asynccontextmanager
async def lifespan(app):
    # Runs once when the app starts.
    create_table()
    yield


app = FastAPI(title="Supplier Cleaner", lifespan=lifespan)


class SupplierIn(BaseModel):
    """The shape of a messy record sent to the API. Every field is optional."""
    name: Optional[str] = None
    email: Optional[str] = None
    price: Optional[str] = None
    date: Optional[str] = None


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/clean")
def clean(supplier: SupplierIn):
    return clean_record(supplier.model_dump())


@app.post("/suppliers")
def add_supplier(supplier: SupplierIn):
    cleaned = clean_record(supplier.model_dump())
    with get_connection() as conn:
        row = conn.execute(
            "INSERT INTO suppliers (name, email, price, date) "
            "VALUES (%s, %s, %s, %s) RETURNING id",
            (cleaned["name"], cleaned["email"], cleaned["price"], cleaned["date"]),
        ).fetchone()
    return {"id": row[0], **cleaned}


@app.get("/suppliers")
def list_suppliers():
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, name, email, price, date FROM suppliers ORDER BY id"
        ).fetchall()
    return [
        {
            "id": r[0],
            "name": r[1],
            "email": r[2],
            "price": float(r[3]) if r[3] is not None else None,
            "date": r[4].isoformat() if r[4] else None,
        }
        for r in rows
    ]
