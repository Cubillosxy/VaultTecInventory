# src/inventory/interfaces/http/router.py
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from inventory.interfaces.http.security import require_user
from inventory.interfaces.http.schemas.products import ProductIn, ProductUpdateIn, ProductOut
from inventory.application.product_create import CreateProduct
from inventory.application.product_update import UpdateProduct
from inventory.application.product_delete import DeleteProduct
from inventory.application.product_list import ListProducts
from inventory.interfaces.http.deps import uow_dep

router = APIRouter(prefix="/products", tags=["products"])

@router.post("", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(data: ProductIn, uow=Depends(uow_dep), _=Depends(require_user)):
    uc = CreateProduct(uow)
    p = uc(**data.model_dump())
    return ProductOut.from_entity(p)

@router.get("", response_model=List[ProductOut])
def list_products(q: Optional[str] = None, uow=Depends(uow_dep), _=Depends(require_user)):
    uc = ListProducts(uow)
    items = uc(query=q)
    return [ProductOut.from_entity(p) for p in items]

@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: str, uow=Depends(uow_dep), _=Depends(require_user)):
    item = uow.products.get(product_id)
    if not item:
        raise HTTPException(status_code=404, detail="Product not found")
    return ProductOut.from_entity(item)

@router.put("/{product_id}", response_model=ProductOut)
def update_product(product_id: str, data: ProductUpdateIn, uow=Depends(uow_dep), _=Depends(require_user)):
    uc = UpdateProduct(uow)
    p = uc(id=product_id, **data.model_dump())
    if not p:
        raise HTTPException(status_code=404, detail="Product not found")
    return ProductOut.from_entity(p)

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: str, uow=Depends(uow_dep), _=Depends(require_user)):
    uc = DeleteProduct(uow)
    ok = uc(product_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Product not found")
