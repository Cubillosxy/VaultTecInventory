from typing import Sequence
from inventory.domain.entities import Product

class ListProducts:
    def __init__(self, uow):
        self.uow = uow

    def __call__(self, query: str | None = None) -> Sequence[Product]:
        return self.uow.products.list(query)
