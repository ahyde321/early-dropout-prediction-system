from fastapi import APIRouter, Depends, HTTPException, status, Header, Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

from db.database import SessionLocal
from db.models import User
from api.schemas import Token, UserCreate, UserResponse, RoleUpdateRequest, UserUpdateRequest

import os

# Define new schemas for password change and settings
class PasswordChangeRequest(BaseModel):
    user_id: int
    current_password: str
    new_password: str

class NotificationSettings(BaseModel):
    emailEnabled: bool = True
    highRiskAlerts: bool = True
    systemUpdates: bool = False

class UserSettingsRequest(BaseModel):
    user_id: int
    notifications: NotificationSettings

router = APIRouter()

# === Security Settings ===
SECRET_KEY = os.getenv("JWT_SECRET", "super-secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# === Utility Functions ===
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, user: User, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({
        "exp": expire,
        "token_version": user.token_version,
    })
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# === Auth Dependencies ===
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        token_version: int = payload.get("token_version")
        if email is None or token_version is None:
            raise credentials_exception
    except JWTError as e:
        print(f"JWT Error: {e}")
        raise credentials_exception

    user = db.query(User).filter(User.email == email).first()
    if user is None or user.token_version != token_version:
        raise credentials_exception

    return user

def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return current_user

# === Auth Routes ===
@router.post("/auth/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.email}, user=user)
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/auth/register", response_model=Token)
def register(
    user_data: UserCreate = Body(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
        first_name=user_data.first_name,
        last_name=user_data.last_name
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    access_token = create_access_token(data={"sub": user.email}, user=user)
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/auth/refresh", response_model=Token)
def refresh_token(authorization: str = Header(...), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not authorization.startswith("Bearer "):
        raise credentials_exception

    token = authorization.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception

    new_token = create_access_token(data={"sub": user.email}, user=user)
    return {"access_token": new_token, "token_type": "bearer"}

@router.post("/auth/logout")
def logout(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    current_user.token_version += 1
    db.commit()
    return {"message": "Logged out. All current tokens are now invalid."}

@router.get("/auth/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

# === New User Settings Routes ===
@router.put("/auth/user/edit")
def edit_user_profile(request: UserUpdateRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Check if user is attempting to edit their own profile or is an admin
    if current_user.id != request.user_id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="You can only edit your own profile unless you're an admin")
    
    user = db.query(User).filter(User.id == request.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if request.first_name: user.first_name = request.first_name
    if request.last_name: user.last_name = request.last_name
    if request.email:
        existing = db.query(User).filter(User.email == request.email).first()
        if existing and existing.id != user.id:
            raise HTTPException(status_code=400, detail="Email already taken")
        user.email = request.email
    if request.role and current_user.role == "admin": 
        user.role = request.role
    if request.is_active is not None and current_user.role == "admin": 
        user.is_active = request.is_active

    db.commit()
    
    # If user updated their own email, invalidate their current token to force re-login
    if request.email and current_user.id == request.user_id:
        user.token_version += 1
        db.commit()
        return {"message": "Profile updated successfully. Please log in again with your new email."}
    
    return {"message": "Profile updated successfully"}

@router.post("/auth/change-password")
def change_password(request: PasswordChangeRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Check if user is attempting to change their own password or is an admin
    if current_user.id != request.user_id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="You can only change your own password unless you're an admin")
    
    user = db.query(User).filter(User.id == request.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check current password - only required if changing own password
    if current_user.id == user.id and not verify_password(request.current_password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    
    # Check password requirements
    if len(request.new_password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters long")
    
    # Update password
    user.hashed_password = get_password_hash(request.new_password)
    
    # Invalidate all existing tokens by incrementing token_version
    user.token_version += 1
    db.commit()
    
    return {"message": "Password changed successfully"}

@router.get("/auth/settings")
def get_user_settings(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # In a real app, you would retrieve settings from a database table
    # For now, we'll return a default if no settings exist
    return {
        "notifications": {
            "emailEnabled": True,
            "highRiskAlerts": True,
            "systemUpdates": False
        }
    }

@router.post("/auth/settings")
def save_user_settings(settings: UserSettingsRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Check if user is attempting to change their own settings or is an admin
    if current_user.id != settings.user_id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="You can only update your own settings unless you're an admin")
    
    # In a real app, you would save these settings to a database table
    # For now, we'll just return success
    return {"message": "Settings updated successfully"}

# === Admin Routes ===
@router.post("/auth/set-role")
def set_user_role(request: RoleUpdateRequest, db: Session = Depends(get_db), admin_user: User = Depends(require_admin)):
    user = db.query(User).filter(User.id == request.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.role = request.role
    db.commit()
    return {"message": f"User {user.email} role updated to {user.role}"}

@router.get("/admin/users", response_model=List[UserResponse])
def list_users(db: Session = Depends(get_db), admin_user: User = Depends(require_admin)):
    return db.query(User).all()

@router.put("/admin/user/edit")
def edit_user(request: UserUpdateRequest, db: Session = Depends(get_db), admin_user: User = Depends(require_admin)):
    user = db.query(User).filter(User.id == request.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if request.first_name: user.first_name = request.first_name
    if request.last_name: user.last_name = request.last_name
    if request.email:
        existing = db.query(User).filter(User.email == request.email).first()
        if existing and existing.id != user.id:
            raise HTTPException(status_code=400, detail="Email already taken")
        user.email = request.email
    if request.role: user.role = request.role
    if request.is_active is not None: user.is_active = request.is_active

    db.commit()
    return {"message": f"User {user.id} updated successfully"}

@router.delete("/admin/user/delete/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), admin_user: User = Depends(require_admin)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"message": f"User {user.email} deleted successfully"}

# === Test Endpoints for Debugging ===
@router.get("/auth/test", response_model=dict)
def test_auth(current_user: User = Depends(get_current_user)):
    """Test endpoint to verify authentication is working properly"""
    return {
        "message": "Authentication successful",
        "user_id": current_user.id,
        "email": current_user.email,
        "role": current_user.role
    }
