from typing import Generator
from inventory.infrastructure.db.sqlite_db import SQLiteUoW

def uow_dep() -> Generator[SQLiteUoW, None, None]:
    uow = SQLiteUoW()
    ctx = uow.__enter__() 
    try:
        yield ctx
    finally:
        ctx.__exit__(None, None, None)
