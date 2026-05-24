import os, httpx
from google.oauth2 import id_token
from google.auth.transport import requests

from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.user import User
from app.utils.jwt import create_access_token, create_refresh_token


GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")


# Google OAuth
def google_login(db: Session, token: str):
    try:
        idinfo = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            GOOGLE_CLIENT_ID
        )

        email = idinfo.get("email")
        name = idinfo.get("name")

        if not email:
            raise HTTPException(status_code=400, detail="Invalid Google token")

    except Exception:
        raise HTTPException(status_code=401, detail="Invalid Google token")

    # Check user exists
    user = db.query(User).filter(User.email == email).first()

    if not user:
        # Create new user
        user = User(
            email=email,
            username=name,
            password_hash="",
            provider="google"
        )

        db.add(user)
        db.commit()
        db.refresh(user)

    # Generate JWT
    access_token = create_access_token({"user_id": str(user.id)})
    refresh_token = create_refresh_token({"user_id": str(user.id)})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }


# Github OAuth
def github_login(db: Session, code: str):
    # Exchange code for access token
    token_response = httpx.post(
        "https://github.com/login/oauth/access_token",
        headers={"Accept": "application/json"},
        data={
            "client_id": GITHUB_CLIENT_ID,
            "client_secret": GITHUB_CLIENT_SECRET,
            "code": code,
        },
    )

    token_json = token_response.json()
    access_token = token_json.get("access_token")

    if not access_token:
        raise HTTPException(status_code=400, detail="GitHub token error")

    # Get user info
    user_response = httpx.get(
        "https://api.github.com/user",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    user_data = user_response.json()

    email = user_data.get("email")
    username = user_data.get("login")

    if not email:
        # Fetch emails separately
        email_resp = httpx.get(
            "https://api.github.com/user/emails",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        emails = email_resp.json()
        email = None
        for e in emails:
            if e.get("primary") and e.get("verified"):
                email = e["email"]
                break

    if not email:
        raise HTTPException(status_code=400, detail="Email not available")

    # Check user
    user = db.query(User).filter(User.email == email).first()

    if not user:
        user = User(
            email=email,
            username=username,
            password_hash="",
            provider="github"
        )

        db.add(user)
        db.commit()
        db.refresh(user)

    # Generate JWT
    access_token = create_access_token({"user_id": str(user.id)})
    refresh_token = create_refresh_token({"user_id": str(user.id)})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }