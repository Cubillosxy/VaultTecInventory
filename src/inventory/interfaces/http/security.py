import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt import InvalidTokenError as JWTError 

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
ALGORITHM = os.getenv("JWT_ALG", "HS256")
SECRET_KEY = os.getenv("JWT_SECRET")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRES_MIN", "60"))

def require_user(token: str = Depends(oauth2_scheme)) -> dict:
    if not SECRET_KEY:
        raise HTTPException(status_code=500, detail="JWT secret not configured")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    if "sub" not in payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
    return payload

def create_access_token(subject: str, extra_claims: Dict[str, Any] | None = None) -> str:
    if not SECRET_KEY:
        raise RuntimeError("JWT secret not configured")
    now = datetime.now(timezone.utc)
    to_encode = {
        "sub": subject,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)).timestamp()),
    }
    if extra_claims:
        to_encode.update(extra_claims)
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
