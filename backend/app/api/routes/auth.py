from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from supabase import create_client
from app.core.config import settings

router = APIRouter()
supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

class RegisterRequest(BaseModel):
    email: str
    password: str
    full_name: str

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/register")
def register(req: RegisterRequest):
    try:
        res = supabase.auth.sign_up({
            "email": req.email,
            "password": req.password,
            "options": {"data": {"full_name": req.full_name}}
        })
        return {"message": "Registered successfully", "user": res.user.email}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
def login(req: LoginRequest):
    try:
        res = supabase.auth.sign_in_with_password({
            "email": req.email,
            "password": req.password
        })
        return {
            "access_token": res.session.access_token,
            "token_type": "bearer",
            "user": res.user.email
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@router.get("/me")
def get_me(token: str):
    try:
        user = supabase.auth.get_user(token)
        return {"email": user.user.email, "id": user.user.id}
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")