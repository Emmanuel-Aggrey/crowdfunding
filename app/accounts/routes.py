from app.core.dependency_injection import service_locator
from sqlalchemy.orm import Session
from fastapi import status
from fastapi import HTTPException
from app.dependencies import get_db
from app.authentication.utils import create_access_token
from app.authentication.utils import authenticate_user
from app.accounts import schemas

from app.accounts.schemas import UserResponseSchema
from app.authentication.utils import get_current_active_user
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Request
from .schemas import UserSchema


router = APIRouter()


@router.post("/register/", response_model=UserResponseSchema)
async def register(
    registation_form: schemas.UserRegistrationForm, db: Session = Depends(get_db)
):
    try:

        user = service_locator.user_service.create_user(db, registation_form)

        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/login/", response_model=schemas.Token)
async def gimme_jwt(
    form_data: schemas.LoginForm, db: Session = Depends(get_db)
) -> schemas.Token:
    user = authenticate_user(form_data.email, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.email})
    return schemas.Token(access_token=access_token, token_type="bearer")


@router.get("/me/", response_model=UserResponseSchema)
async def get_account(request: Request, user: UserSchema = Depends(get_current_active_user)):
    current_user: UserSchema = request.state.user
    return current_user
