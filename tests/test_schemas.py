import pytest
from pydantic import ValidationError

from inventory.domain.entities import Product
from inventory.interfaces.http.schemas.products import (
    ProductIn, ProductUpdateIn, ProductOut
)

def test_productin_validation_errors():
    with pytest.raises(ValidationError):
        ProductIn(name="", description="x", price=10.0, quantity=1)  # name too short
    with pytest.raises(ValidationError):
        ProductIn(name="A", description="x", price=-1, quantity=1)   # negative price
    with pytest.raises(ValidationError):
        ProductIn(name="A", description="x", price=10, quantity=-5)  # negative qty

def test_productout_from_entity():
    entity = Product(
        id="01JABCDETESTIDXYZ12345678",
        name="Mouse",
        description="Wireless",
        price=19.9,
        quantity=10,
        image_url=None,
    )
    out = ProductOut.from_entity(entity)
    assert out.id == entity.id
    assert out.name == "Mouse"
    assert out.quantity == 10

def test_productupdatein_optional_fields():
    u = ProductUpdateIn()
    assert u.model_dump(exclude_none=True) == {}
    u2 = ProductUpdateIn(name="X")
    assert u2.name == "X"
