from inventory.domain.ports.product_repo import ProductRepository
from inventory.domain.ports.unit_of_work import UnitOfWork

class DeleteProduct:
    def __init__(self, repo: ProductRepository, uow: UnitOfWork):
        self.repo, self.uow = repo, uow
    def __call__(self, pid: int) -> bool:
        with self.uow:
            ok = self.repo.delete(pid)
            if ok: self.uow.commit()
            return ok
