from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from inventory.interfaces.http.auth import auth_router
from inventory.interfaces.http.router import router as products_router

app = FastAPI(title="Inventory API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(products_router)
