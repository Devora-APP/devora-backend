from pydantic import BaseModel, EmailStr

#  Register request
class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str


#  Login request
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


#  Token response
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


# Change Password
class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str