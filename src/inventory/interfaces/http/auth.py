
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from inventory.interfaces.http.security import create_access_token

auth_router = APIRouter(prefix="/auth", tags=["auth"])

# Dummy credential check for now.
# Replace with your real user storage (SQLite table, etc.)
def verify_user(username: str, password: str) -> bool:
    # Example: accept a single dev user from env, or anything non-empty in dev
    from os import getenv
    dev_user = getenv("DEV_USER", "test")
    dev_pass = getenv("DEV_PASS", "test")
    if dev_user and dev_pass:
        return username == dev_user and password == dev_pass
    # fallback: require non-empty (dev only)
    return bool(username and password)

@auth_router.post("/token")
def issue_token(form: OAuth2PasswordRequestForm = Depends()):
    if not verify_user(form.username, form.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(subject=form.username)
    return {"access_token": token, "token_type": "bearer"}
