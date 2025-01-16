import typing

from sqlalchemy.orm import Session
from . import models

if typing.TYPE_CHECKING:
    from app.accounts.schemas import UserRegistrationForm


class UserService:
    def get_user(self, db: Session, user_id: int):
        return db.query(models.User).filter(models.User.id == user_id).first()

    def get_user_by_email(self, db: Session, email: str):
        return db.query(models.User).filter(models.User.email == email).first()

    def get_users(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.User).offset(skip).limit(limit).all()

    def create_user(self, db: Session, user: "UserRegistrationForm"):
        from app.authentication.utils import get_password_hash

        hashed_password = get_password_hash(user.password)
        if db.query(models.User).filter(models.User.email == user.email).first():
            raise ValueError("User already exists")

        db_user = models.User(
            email=user.email, username=user.username, hashed_password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
