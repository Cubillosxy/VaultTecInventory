import os
import psycopg
from typing import Sequence
from inventory.domain.entities import Product

class PgUoW:
    def __init__(self, dsn: str | None = None):
        self.dsn = dsn or os.getenv("PG_DSN", "postgresql://inventory:inventory@localhost:5432/inventory")
        self.conn: psycopg.Connection | None = None

    def __enter__(self):
        self.conn = psycopg.connect(self.dsn, autocommit=False)
        with self.conn.cursor() as cur:
            cur.execute(
                "CREATE TABLE IF NOT EXISTS products ("
                "id SERIAL PRIMARY KEY,"
                "name TEXT UNIQUE,"
                "description TEXT,"
                "price DOUBLE PRECISION,"
                "quantity INTEGER,"
                "image_url TEXT)"
            )
        return self

    def __exit__(self, exc_type, exc, tb):
        if self.conn:
            if exc_type:
                self.conn.rollback()
            self.conn.close()

    @property
    def products(self):
        return PgProductRepo(self.conn)

    def commit(self): self.conn.commit()
    def rollback(self): self.conn.rollback()

class PgProductRepo:
    def __init__(self, conn: psycopg.Connection):
        self.conn = conn

    def list(self, search: str | None = None) -> Sequence[Product]:
        with self.conn.cursor() as cur:
            if search:
                cur.execute(
                    "SELECT id,name,description,price,quantity,image_url FROM products WHERE name ILIKE %s",
                    (f"%{search}%",)
                )
            else:
                cur.execute("SELECT id,name,description,price,quantity,image_url FROM products")
            return [Product(*row) for row in cur.fetchall()]

    def get(self, pid: int) -> Product | None:
        with self.conn.cursor() as cur:
            cur.execute("SELECT id,name,description,price,quantity,image_url FROM products WHERE id=%s", (pid,))
            row = cur.fetchone()
            return Product(*row) if row else None

    def create(self, p: Product) -> Product:
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO products(name,description,price,quantity,image_url) VALUES(%s,%s,%s,%s,%s) RETURNING id",
                (p.name, p.description, p.price, p.quantity, p.image_url)
            )
            pid = cur.fetchone()[0]
            return Product(pid, p.name, p.description, p.price, p.quantity, p.image_url)

    def update(self, p: Product) -> Product | None:
        with self.conn.cursor() as cur:
            cur.execute(
                "UPDATE products SET name=%s, description=%s, price=%s, quantity=%s, image_url=%s WHERE id=%s",
                (p.name, p.description, p.price, p.quantity, p.image_url, p.id)
            )
            return p if cur.rowcount else None

    def delete(self, pid: int) -> bool:
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM products WHERE id=%s", (pid,))
            return cur.rowcount > 0
