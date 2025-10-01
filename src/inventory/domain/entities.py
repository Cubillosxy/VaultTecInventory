from dataclasses import dataclass

@dataclass(frozen=True)
class Product:
    id: str | None
    name: str
    description: str
    price: float
    quantity: int
    image_url: str | None = None
