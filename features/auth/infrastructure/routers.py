from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from core.db.connection import get_db
from core.config.settings import settings
from features.auth.infrastructure.repositories import UserRepositoryImpl
from features.auth.application.schemas import LoginRequest, RegisterRequest, TokenResponse, UserResponse
from features.auth.application.usecases import AuthUseCases

router = APIRouter()

def get_auth_usecases(db: Session = Depends(get_db)):
    repo = UserRepositoryImpl(db)
    return AuthUseCases(repo)

@router.post("/auth/login", response_model=TokenResponse, tags=["Auth"])
def login(req: LoginRequest, uc: AuthUseCases = Depends(get_auth_usecases)):
    try:
        return uc.login(req)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.post("/auth/register", response_model=UserResponse, tags=["Auth"])
def register(req: RegisterRequest, uc: AuthUseCases = Depends(get_auth_usecases)):
    try:
        return uc.register(req)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/internal/users/{id_usuario}", response_model=UserResponse, tags=["Internal"])
def get_internal_user_info(
    id_usuario: str, 
    x_api_key: str = Header(default=settings.API_KEY),
    uc: AuthUseCases = Depends(get_auth_usecases)
):
    if x_api_key != settings.API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    try:
        return uc.get_user_info(id_usuario)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/internal/users", response_model=list[UserResponse], tags=["Internal"])
def get_all_users(
    rol: str = None,
    x_api_key: str = Header(default=settings.API_KEY),
    uc: AuthUseCases = Depends(get_auth_usecases)
):
    if x_api_key != settings.API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return uc.get_all_users(rol)
