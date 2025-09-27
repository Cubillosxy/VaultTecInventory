from inventory.domain.entities import Product
from inventory.domain.ports.product_repo import ProductRepository
from inventory.domain.ports.unit_of_work import UnitOfWork

class CreateProduct:
    def __init__(self, repo: ProductRepository, uow: UnitOfWork):
        self.repo, self.uow = repo, uow
    def __call__(self, name: str, description: str, price: float, quantity: int, image_url: str | None = None) -> Product:
        p = Product(None, name, description, price, quantity, image_url)
        with self.uow:
            out = self.repo.create(p)
            self.uow.commit()
            return out
