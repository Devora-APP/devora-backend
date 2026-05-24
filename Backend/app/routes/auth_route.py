from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.core.dependencies import get_db

from app.schemas.auth import (RegisterRequest, LoginRequest, TokenResponse)
from app.schemas.user import UserResponse
from app.services.auth_service import (register_user, login_user, change_password)
from app.schemas.auth import ChangePasswordRequest
from app.schemas.oauth import GoogleAuthRequest, GitHubAuthRequest
from app.services.oauth_service import google_login, github_login


router = APIRouter(prefix="/auth", tags=["Auth"])

# Register User
@router.post("/register", response_model=UserResponse)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    try:
        user = register_user(db, data)
        return user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Login User
@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    try:
        tokens = login_user(db, data)
        return tokens
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
        

# Get Current User
@router.get("/me", response_model=UserResponse)
def get_me(current_user = Depends(get_current_user)):
    return current_user


# Change Password
@router.post("/change-password")
def change_password_api(
    data: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    change_password(db, current_user, data)
    return {"message": "Password updated successfully"}


# OAUTH Login
# Google
@router.post("/google")
def google_auth(
    data: GoogleAuthRequest,
    db: Session = Depends(get_db)
):
    return google_login(db, data.token)

# GitHub 
@router.post("/github")
def github_auth(
    data: GitHubAuthRequest,
    db: Session = Depends(get_db)
):
    return github_login(db, data.code)