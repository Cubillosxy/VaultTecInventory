from inventory.domain.entities import Product
from inventory.usecases.product_create import CreateProduct
from inventory.usecases.product_list import ListProducts
from inventory.usecases.product_update import UpdateProduct
from inventory.usecases.product_delete import DeleteProduct

class FakeRepo:
    def __init__(self):
        self.data = {}
        self.auto = 1
    def list(self, search=None):
        v = list(self.data.values())
        return [x for x in v if search and search.lower() in x.name.lower()] if search else v
    def get(self, pid):
        return self.data.get(pid)
    def create(self, p):
        q = Product(self.auto, p.name, p.description, p.price, p.quantity, p.image_url)
        self.data[self.auto] = q
        self.auto += 1
        return q
    def update(self, p):
        if p.id not in self.data: return None
        self.data[p.id] = p; return p
    def delete(self, pid):
        return self.data.pop(pid, None) is not None

class DummyUoW:
    def __enter__(self): return self
    def __exit__(self, *a): ...
    @property
    def products(self): return None
    def commit(self): ...
    def rollback(self): ...

def test_crud_flow():
    repo, uow = FakeRepo(), DummyUoW()
    created = CreateProduct(repo, uow)("Mouse", "Wireless", 19.9, 10, None)
    assert created.id == 1
    assert len(ListProducts(repo, uow)()) == 1
    updated = UpdateProduct(repo, uow)(1, "Mouse Pro", "Wireless", 29.9, 5, None)
    assert updated and updated.name == "Mouse Pro"
    assert DeleteProduct(repo, uow)(1) is True
    assert len(ListProducts(repo, uow)()) == 0
