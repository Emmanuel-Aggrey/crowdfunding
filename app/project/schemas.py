
from app.core.schema import BaseSchema
from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional, List
from pydantic import Field
from app.accounts.schemas import UserResponseSchema
from uuid import UUID
from decimal import Decimal


class ProjectCreateSchema(BaseModel):
    title: str
    description: Optional[str] = ""
    goal_amount: float = Field(..., gt=0)
    deadline: date

    class Config:
        from_attributes = True


class ProjectResponseSchema(BaseSchema, BaseModel):
    title: str
    description: Optional[str] = ""
    goal_amount: float = Field(..., gt=0)
    deadline: datetime
    total_contribution: Optional[Decimal] = 0
    contributors: List[UserResponseSchema] = []

    class Config:
        from_attributes = True


class ProjectContributeSchema(BaseModel):

    contribution_amount: float = Field(..., gt=0)

    class Config:
        from_attributes = True


class ContributionSchema(BaseModel):
    amount: float = Field(..., gt=0)
    user: UserResponseSchema
    project_id: UUID
