import os
import sqlite3
import uuid
from typing import Sequence
from inventory.domain.entities import Product

class SQLiteUoW:
    def __init__(self, path: str | None = None):
        self.path = path or os.getenv("SQLITE_PATH", "./infrastructure.db")
        self.conn: sqlite3.Connection | None = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.path)
        self.conn.execute("PRAGMA foreign_keys = ON")
        # id is TEXT PRIMARY KEY (UUID or ULID as string)
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS products ("
            "id TEXT PRIMARY KEY,"
            "name TEXT UNIQUE,"
            "description TEXT,"
            "price REAL,"
            "quantity INTEGER,"
            "image_url TEXT)"
        )
        return self

    def __exit__(self, exc_type, exc, tb):
        if not self.conn:
            return False
        try:
            if exc_type:
                self.conn.rollback()
        finally:
            self.conn.close()
        return False

    @property
    def products(self):
        if not self.conn:
            raise RuntimeError("Connection is not initialized. Use within context.")
        return SQLiteProductRepo(self.conn)

    def commit(self):
        if self.conn:
            self.conn.commit()

    def rollback(self):
        if self.conn:
            self.conn.rollback()


class SQLiteProductRepo:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def list(self, search: str | None = None) -> Sequence[Product]:
        if search:
            rows = self.conn.execute(
                "SELECT id,name,description,price,quantity,image_url FROM products WHERE name LIKE ?",
                (f"%{search}%",)
            ).fetchall()
        else:
            rows = self.conn.execute(
                "SELECT id,name,description,price,quantity,image_url FROM products"
            ).fetchall()
        return [Product(*row) for row in rows]

    def get(self, pid: str) -> Product | None:
        row = self.conn.execute(
            "SELECT id,name,description,price,quantity,image_url FROM products WHERE id=?",
            (pid,)
        ).fetchone()
        return Product(*row) if row else None

    def create(self, p: Product) -> Product:
        # generate UUID if not provided
        pid = p.id or str(uuid.uuid4())
        self.conn.execute(
            "INSERT INTO products(id,name,description,price,quantity,image_url) VALUES(?,?,?,?,?,?)",
            (pid, p.name, p.description, p.price, p.quantity, p.image_url)
        )
        return Product(pid, p.name, p.description, p.price, p.quantity, p.image_url)

    def update(self, p: Product) -> Product | None:
        cur = self.conn.execute(
            "UPDATE products SET name=?, description=?, price=?, quantity=?, image_url=? WHERE id=?",
            (p.name, p.description, p.price, p.quantity, p.image_url, p.id)
        )
        return p if cur.rowcount else None

    def delete(self, pid: str) -> bool:
        cur = self.conn.execute("DELETE FROM products WHERE id=?", (pid,))
        return cur.rowcount > 0
