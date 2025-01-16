from datetime import datetime
from datetime import timedelta
from datetime import timezone
from typing import Annotated
import jwt
from app.accounts.schemas import UserSchema
from app.dependencies import get_db
from app.settings import ACCESS_TOKEN_EXPIRE
from app.settings import ALGORITHM
from app.settings import SECRET_KEY
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from fastapi import status
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.core.dependency_injection import service_locator
from app.accounts.schemas import TokenData
from app.authentication.enum import TimeUnit
router = APIRouter()
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(email: str, db: Session):

    user = service_locator.user_service.get_user_by_email(db, email)
    if user:
        return user


def authenticate_user(email: str, password: str, db: Session):
    user = get_user(email, db)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None,
    expire_time: int = ACCESS_TOKEN_EXPIRE,
    unit: str = TimeUnit.DAYS,
) -> dict:
    if expires_delta is None:
        expires_delta = calculate_expiration_time(expire_time, unit)

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})

    # Encode the JWT token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def calculate_expiration_time(expire_time: int, unit: TimeUnit) -> timedelta:
    if unit == TimeUnit.MINUTES:
        return timedelta(minutes=expire_time)
    elif unit == TimeUnit.HOURS:
        return timedelta(hours=expire_time)
    elif unit == TimeUnit.DAYS:
        return timedelta(days=expire_time)
    else:
        raise ValueError(
            "Invalid unit for expiration time. Use 'minutes', 'hours', or 'days'."
        )


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="gimme-jwt")

auth_scheme = HTTPBearer()


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(auth_scheme)],
    db: Session = Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid token or token expired",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except Exception:
        raise credentials_exception

    user = service_locator.user_service.get_user_by_email(db, token_data.email)

    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[UserSchema, Depends(get_current_user)], request: Request
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    request.state.user = current_user
    return current_user
