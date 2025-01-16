from app.core.models import BaseModel
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy.orm import relationship


class User(BaseModel):
    __tablename__ = "users"
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    username = Column(String)

    contributions = relationship("Contribution", back_populates="user")
