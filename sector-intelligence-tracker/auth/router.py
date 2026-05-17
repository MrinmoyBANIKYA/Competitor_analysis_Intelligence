import os
import uuid
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_db
from db import crud, models

# Secrets Configuration
SECRET_KEY = os.getenv("JWT_SECRET", "nixtio_super_secret_key_2026_hs256")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 24 * 60  # 24 hours
REFRESH_TOKEN_EXPIRE_DAYS = 30  # 30 days

# Password Cryptography
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False

# OAuth2 Scheme definition
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=False)

# Router
router = APIRouter(prefix="/auth", tags=["Authentication"])

# --- Pydantic Request/Response Schemas ---
class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    org_name: str
    plan_tier: Optional[str] = "free"

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class UserContextResponse(BaseModel):
    id: int
    email: str
    role: str
    org_id: int
    org_name: str
    plan_tier: str

class RefreshRequest(BaseModel):
    refresh_token: str

# --- JWT Helpers ---
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# --- Get Current User Dependency ---
async def get_current_user(token: Optional[str] = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not token:
        raise credentials_exception
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id_str = payload.get("sub")
        if user_id_str is None:
            raise credentials_exception
        user_id = int(user_id_str)
    except (JWTError, ValueError):
        raise credentials_exception
        
    # Query database for user
    from sqlalchemy.future import select
    result = await db.execute(
        select(models.User).where(models.User.id == user_id)
    )
    user = result.scalars().first()
    if user is None:
        raise credentials_exception
    return user

# --- Routes ---

@router.post("/register", response_model=TokenResponse)
async def register(request: RegisterRequest, db: AsyncSession = Depends(get_db)):
    # Check if user already exists
    existing_user = await crud.get_user_by_email(db, request.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
        
    # Validate plan tier
    if request.plan_tier not in ["free", "pro", "enterprise"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid plan tier specified"
        )
        
    # Create Org
    mock_api_key_hash = str(uuid.uuid4())
    org = await crud.create_org(
        db, 
        name=request.org_name, 
        api_key_hash=mock_api_key_hash, 
        plan_tier=request.plan_tier
    )
    
    # Create User
    hashed_pwd = hash_password(request.password)
    user = await crud.create_user(
        db,
        email=request.email,
        hashed_password=hashed_pwd,
        org_id=org.id,
        role="admin"  # First registered user of an org becomes admin
    )
    
    # Generate Tokens
    token_claims = {"sub": str(user.id), "email": user.email, "org_id": org.id}
    access_token = create_access_token(data=token_claims)
    
    refresh_token_val = str(uuid.uuid4())
    expires_at = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    await crud.create_refresh_token(db, user_id=user.id, token=refresh_token_val, expires_at=expires_at)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token_val,
        "token_type": "bearer"
    }

@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    user = await crud.get_user_by_email(db, request.email)
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    # Retrieve org details
    from sqlalchemy.future import select
    org_res = await db.execute(select(models.Org).where(models.Org.id == user.org_id))
    org = org_res.scalars().first()
    
    # Generate Tokens
    token_claims = {"sub": str(user.id), "email": user.email, "org_id": user.org_id}
    access_token = create_access_token(data=token_claims)
    
    refresh_token_val = str(uuid.uuid4())
    expires_at = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    await crud.create_refresh_token(db, user_id=user.id, token=refresh_token_val, expires_at=expires_at)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token_val,
        "token_type": "bearer"
    }

@router.post("/refresh", response_model=TokenResponse)
async def refresh(request: RefreshRequest, db: AsyncSession = Depends(get_db)):
    db_token = await crud.get_refresh_token(db, request.refresh_token)
    if not db_token or db_token.expires_at < datetime.utcnow():
        if db_token:
            await crud.delete_refresh_token(db, request.refresh_token)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )
        
    # Fetch User
    from sqlalchemy.future import select
    user_res = await db.execute(select(models.User).where(models.User.id == db_token.user_id))
    user = user_res.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
        
    # Rotate refresh token
    await crud.delete_refresh_token(db, request.refresh_token)
    
    new_refresh_val = str(uuid.uuid4())
    new_expires_at = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    await crud.create_refresh_token(db, user_id=user.id, token=new_refresh_val, expires_at=new_expires_at)
    
    # Generate new access token
    token_claims = {"sub": str(user.id), "email": user.email, "org_id": user.org_id}
    new_access_token = create_access_token(data=token_claims)
    
    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_val,
        "token_type": "bearer"
    }

@router.get("/me", response_model=UserContextResponse)
async def me(user: models.User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    from sqlalchemy.future import select
    org_res = await db.execute(select(models.Org).where(models.Org.id == user.org_id))
    org = org_res.scalars().first()
    
    return {
        "id": user.id,
        "email": user.email,
        "role": user.role,
        "org_id": user.org_id,
        "org_name": org.name if org else "Unknown",
        "plan_tier": org.plan_tier if org else "free"
    }
