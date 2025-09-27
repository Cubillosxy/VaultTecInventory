from inventory.domain.entities import Product
from inventory.domain.ports.product_repo import ProductRepository
from inventory.domain.ports.unit_of_work import UnitOfWork

class UpdateProduct:
    def __init__(self, repo: ProductRepository, uow: UnitOfWork) -> None:
        self.repo, self.uow = repo, uow
    def __call__(self, pid: int, name: str, description: str, price: float, quantity: int, image_url: str | None = None) -> Product | None:
        with self.uow:
            existing = self.repo.get(pid)
            if not existing:
                return None
            updated = Product(pid, name, description, price, quantity, image_url)
            out = self.repo.update(updated)
            self.uow.commit()
            return out
