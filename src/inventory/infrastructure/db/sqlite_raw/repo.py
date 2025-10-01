import os
import sqlite3
from typing import Sequence
from inventory.domain.entities import Product

class SQLiteUoW:
    def __init__(self, path: str | None = None):
        self.path = path or os.getenv("SQLITE_PATH", "./app.db")
        self.conn: sqlite3.Connection | None = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.path)
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS products ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "name TEXT UNIQUE,"
            "description TEXT,"
            "price REAL,"
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
        return SQLiteProductRepo(self.conn)

    def commit(self): self.conn.commit()
    def rollback(self): self.conn.rollback()

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

    def get(self, pid: int) -> Product | None:
        row = self.conn.execute(
            "SELECT id,name,description,price,quantity,image_url FROM products WHERE id=?",
            (pid,)
        ).fetchone()
        return Product(*row) if row else None

    def create(self, p: Product) -> Product:
        cur = self.conn.execute(
            "INSERT INTO products(name,description,price,quantity,image_url) VALUES(?,?,?,?,?)",
            (p.name, p.description, p.price, p.quantity, p.image_url)
        )
        pid = cur.lastrowid
        return Product(pid, p.name, p.description, p.price, p.quantity, p.image_url)

    def update(self, p: Product) -> Product | None:
        cur = self.conn.execute(
            "UPDATE products SET name=?, description=?, price=?, quantity=?, image_url=? WHERE id=?",
            (p.name, p.description, p.price, p.quantity, p.image_url, p.id)
        )
        return p if cur.rowcount else None

    def delete(self, pid: int) -> bool:
        cur = self.conn.execute("DELETE FROM products WHERE id=?", (pid,))
        return cur.rowcount > 0
