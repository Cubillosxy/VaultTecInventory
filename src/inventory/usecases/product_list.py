from typing import Sequence
from inventory.domain.entities import Product
from inventory.domain.ports.product_repo import ProductRepository
from inventory.domain.ports.unit_of_work import UnitOfWork

class ListProducts:
    def __init__(self, repo: ProductRepository, uow: UnitOfWork):
        self.repo, self.uow = repo, uow
    def __call__(self, search: str | None = None) -> Sequence[Product]:
        with self.uow:
            return self.repo.list(search)
