from ulid import new as ulid_new
from inventory.domain.entities import Product

class CreateProduct:
    def __init__(self, uow):
        self.uow = uow

    def __call__(self, name: str, description: str = "", price: float = 0.0,
                 quantity: int = 0, image_url: str | None = None) -> Product:
        # id is autoincrement, so pass a placeholder (0 or None) in the entity constructor
        draft = Product(0, name, description or "", float(price), int(quantity), image_url)
        created = self.uow.products.create(draft)
        self.uow.commit()
        return created