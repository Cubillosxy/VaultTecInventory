from inventory.domain.entities import Product

class UpdateProduct:
    def __init__(self, uow):
        self.uow = uow

    def __call__(self, id: str, name: str, description: str, price: float,
                 quantity: int, image_url: str | None = None) -> Product | None:
        current = self.uow.products.get(id)
        if not current:
            return None
        # build updated entity
        updated = Product(
            id=str(id),
            name=name,
            description=description or "",
            price=float(price),
            quantity=int(quantity),
            image_url=image_url
        )
        saved = self.uow.products.update(updated)
        if saved:
            self.uow.commit()
        return saved