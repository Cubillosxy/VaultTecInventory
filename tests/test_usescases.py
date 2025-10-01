# tests/test_usecases.py
import uuid
import pytest

from inventory.domain.entities import Product
from inventory.application.product_create import CreateProduct
from inventory.application.product_list import ListProducts
from inventory.application.product_update import UpdateProduct
from inventory.application.product_delete import DeleteProduct


# ---- Fakes ----

class FakeRepo:
    def __init__(self):
        self.data: dict[str, Product] = {}

    def list(self, search: str | None = None):
        items = list(self.data.values())
        if not search:
            return items
        s = search.lower()
        return [p for p in items if s in (p.name or "").lower()]

    def get(self, pid: str) -> Product | None:
        return self.data.get(pid)

    def create(self, p: Product) -> Product:
        pid = p.id or str(uuid.uuid4())
        out = Product(
            id=pid,
            name=p.name,
            description=p.description,
            price=float(p.price),
            quantity=int(p.quantity),
            image_url=getattr(p, "image_url", None),
        )
        self.data[pid] = out
        return out

    def update(self, p: Product) -> Product | None:
        if p.id not in self.data:
            return None
        self.data[p.id] = p
        return p

    def delete(self, pid: str) -> bool:
        return self.data.pop(pid, None) is not None


class FakeUoW:
    def __init__(self, repo: FakeRepo):
        self._repo = repo
        self.commits = 0
        self.rollbacks = 0

    def __enter__(self):  # not strictly needed by use-cases, kept for parity
        return self

    def __exit__(self, exc_type, exc, tb):
        if exc_type:
            self.rollback()

    @property
    def products(self) -> FakeRepo:
        return self._repo

    def commit(self):
        self.commits += 1

    def rollback(self):
        self.rollbacks += 1


# ---- Fixtures ----

@pytest.fixture()
def repo_uow():
    repo = FakeRepo()
    uow = FakeUoW(repo)
    return repo, uow


# ---- Tests ----

def test_crud_flow(repo_uow):
    repo, uow = repo_uow

    # create
    created = CreateProduct(uow)(
        name="Mouse", description="Wireless", price=19.9, quantity=10, image_url=None
    )
    assert isinstance(created.id, str) and created.id
    assert created.name == "Mouse"
    assert uow.commits == 1

    # list
    items = ListProducts(uow)()
    assert len(items) == 1
    assert items[0].id == created.id

    # update
    updated = UpdateProduct(uow)(
        id=created.id,
        name="Mouse Pro",
        description="Wireless",
        price=29.9,
        quantity=5,
        image_url=None,
    )
    assert updated is not None
    assert updated.name == "Mouse Pro"
    assert uow.commits == 2

    # delete
    ok = DeleteProduct(uow)(created.id)
    assert ok is True
    assert uow.commits == 3
    assert len(ListProducts(uow)()) == 0


def test_list_search(repo_uow):
    repo, uow = repo_uow
    p1 = CreateProduct(uow)("Keyboard", "Mechanical", 89.9, 10, None)
    p2 = CreateProduct(uow)("Headphones", "NC", 299.0, 3, None)
    _ = CreateProduct(uow)("Mousepad", "XL", 15.0, 40, None)

    all_items = ListProducts(uow)()
    assert {p.id for p in all_items} == {p1.id, p2.id, _ .id}

    filtered = ListProducts(uow)("head")
    names = [p.name for p in filtered]
    assert names == ["Headphones"]


def test_update_not_found(repo_uow):
    _, uow = repo_uow
    missing = UpdateProduct(uow)(
        id="non-existent-id",
        name="X",
        description="Y",
        price=1.0,
        quantity=1,
        image_url=None,
    )
    assert missing is None


def test_delete_not_found(repo_uow):
    _, uow = repo_uow
    assert DeleteProduct(uow)("non-existent-id") is False


def test_repo_get_roundtrip(repo_uow):
    repo, uow = repo_uow
    c = CreateProduct(uow)("Laptop", "Dev", 1200.5, 5, None)
    fetched = repo.get(c.id)
    assert fetched is not None
    assert fetched.id == c.id
    assert fetched.price == pytest.approx(1200.5)
