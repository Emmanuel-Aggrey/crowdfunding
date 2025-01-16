from app.core.models import BaseModel
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import DECIMAL
from sqlalchemy import DateTime
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from sqlalchemy import UUID


class Project(BaseModel):
    __tablename__ = "projects"
    title = Column(String, index=True)
    description = Column(String)
    goal_amount = Column(DECIMAL(10, 2))
    deadline = Column(DateTime)

    contributions = relationship("Contribution", back_populates="project")


class Contribution(BaseModel):
    __tablename__ = "contributions"

    amount = Column(DECIMAL(10, 2))
    user_id = Column(UUID(as_uuid=True), ForeignKey(
        'users.id', ondelete="CASCADE"))
    project_id = Column(UUID(as_uuid=True), ForeignKey(
        'projects.id', ondelete="CASCADE"))

    user = relationship("User", back_populates="contributions")
    project = relationship("Project", back_populates="contributions")
