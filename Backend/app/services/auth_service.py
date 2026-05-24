from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.auth import RegisterRequest, LoginRequest
from app.utils.hash import hash_password, verify_password
from app.utils.jwt import create_access_token, create_refresh_token


# Register User
def register_user(db: Session, data: RegisterRequest):

    # check if user exists
    existing_user = db.query(User).filter(
        (User.email == data.email) | (User.username == data.username)
    ).first()

    if existing_user:
        raise Exception("User already exists")

    # create user
    user = User(
        username=data.username,
        email=data.email,
        password_hash=hash_password(data.password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


# Login User
def login_user(db: Session, data: LoginRequest):
    user = db.query(User).filter(User.email == data.email).first()

    if not user or not verify_password(data.password, user.password_hash):
        raise Exception("Invalid credentials")

    access_token = create_access_token({"user_id": str(user.id)})
    refresh_token = create_refresh_token({"user_id": str(user.id)})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }


# Change Password for existing user
def change_password(db, user, data):
    # Block OAuth users
    if user.provider is not None:
        raise HTTPException(
            status_code=400,
            detail="Password change not allowed for OAuth users"
        )

    # Verify old password
    if not verify_password(data.old_password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect old password")

    # Update password
    user.password_hash = hash_password(data.new_password)

    db.commit()