# microservicios/auth-service/app/security.py
from datetime import datetime, timedelta, timezone
from typing import Optional,Dict
from passlib.context import CryptContext
from jose import JWTError, jwt
from app.core.config import SECRET_KEY, ALGORITHM
from fastapi import Depends, HTTPException, status 
from fastapi.security import OAuth2PasswordBearer 


# Configuración para hashing de contraseñas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

def get_password_hash(password: str) -> str:
    """Hashea una contraseña usando Bcrypt."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica una contraseña contra un hash."""
    return pwd_context.verify(plain_password, hashed_password)



def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Crea un token de acceso JWT."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15) 

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    """Verifica un token JWT y devuelve el payload si es válido, None si no."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None 
    

def get_current_user_payload(
    token: str = Depends(oauth2_scheme), # FastAPI inyecta el token del encabezado
    
) -> Dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # 1. Verificar el token
    payload = verify_token(token)
    if payload is None:
        raise credentials_exception

    # 2. Obtener el email del payload (el "sub" de nuestro token)
    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception
    return payload

   