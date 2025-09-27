import os
from dataclasses import asdict
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, Field
from inventory.infrastructure.db.postgres_raw.repo import PgUoW as UnitOfWork
from inventory.usecases.product_create import CreateProduct
from inventory.usecases.product_list import ListProducts
from inventory.usecases.product_update import UpdateProduct
from inventory.usecases.product_delete import DeleteProduct

app = FastAPI(title="Inventory Clean Backend")

class ProductIn(BaseModel):
    name: str = Field(min_length=1)
    description: str = ""
    price: float = Field(ge=0)
    quantity: int = Field(ge=0)
    image_url: str | None = None

def uow_dep():
    return UnitOfWork(os.getenv("PG_DSN"))

@app.get("/health")
def health():
    return {"status": "ok", "adapter": UnitOfWork.__name__}

@app.get("/products")
def list_products(search: str | None = None, uow = Depends(uow_dep)):
    uc = ListProducts(uow.products, uow)
    out = uc(search)
    return [asdict(p) for p in out]

@app.post("/products", status_code=201)
def create_product(data: ProductIn, uow = Depends(uow_dep)):
    uc = CreateProduct(uow.products, uow)
    p = uc(**data.model_dump())
    return asdict(p)

@app.put("/products/{pid}")
def update_product(pid: int, data: ProductIn, uow = Depends(uow_dep)):
    uc = UpdateProduct(uow.products, uow)
    p = uc(pid, **data.model_dump())
    if not p:
        raise HTTPException(404, "Not found")
    return asdict(p)

@app.delete("/products/{pid}", status_code=204)
def delete_product(pid: int, uow = Depends(uow_dep)):
    uc = DeleteProduct(uow.products, uow)
    ok = uc(pid)
    if not ok:
        raise HTTPException(404, "Not found")
    return {}
