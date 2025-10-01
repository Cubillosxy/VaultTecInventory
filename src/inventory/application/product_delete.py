
class DeleteProduct:
    def __init__(self, uow):
        self.uow = uow

    def __call__(self, id: str) -> bool:
        ok = self.uow.products.delete(id)
        if ok:
            self.uow.commit()
        return ok