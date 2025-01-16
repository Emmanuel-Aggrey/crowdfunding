
from app.accounts.schemas import UserSchema
from app.authentication.utils import get_current_active_user
from app.core.dependency_injection import service_locator
from app.dependencies import get_db
from app.project.models import Project
from app.project.schemas import ProjectCreateSchema, ProjectResponseSchema
from app.project.schemas import ProjectContributeSchema
from fastapi import APIRouter
from fastapi import Depends
from fastapi_pagination import add_pagination
from fastapi_pagination import Page
from fastapi_pagination import paginate
from fastapi_utils.cbv import cbv
from pydantic import UUID4
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException
from fastapi import status
from decimal import Decimal
router = APIRouter()


@cbv(router)
class ProjectView:
    db: Session = Depends(get_db)

    @router.post("/", response_model=ProjectResponseSchema)
    async def projects(self, data: ProjectCreateSchema,
                       current_user: UserSchema = Depends(get_current_active_user)):

        project = Project(
            **data.model_dump(), )

        response = service_locator.general_service.create_data(
            db=self.db, model=project)

        return response

    @router.get("/", response_model=Page[ProjectResponseSchema])
    async def list_projects(self):
        projects = service_locator.general_service.list_data(
            db=self.db, model=Project)

        [self.add_project_additional_data(project) for project in projects]

        return paginate(projects)

    @router.get("/{id}/", response_model=ProjectResponseSchema)
    async def get_project(self, id: UUID4):
        project: ProjectResponseSchema = service_locator.general_service.get_data_by_id(
            self.db, id, Project
        )

        self.add_project_additional_data(project)

        return project

    def add_project_additional_data(self, project: ProjectResponseSchema):
        service_locator.general_service.raise_not_found(project)

        project.contributors = service_locator.project_service.get_contributors(
            self.db, project.id)

        project.total_contribution = service_locator.project_service.get_total_contributions(
            self.db, project.id)

        return project

    @router.post("/{id}/contribute/", response_model=ProjectResponseSchema)
    async def project_contribute(self, id: UUID4, data: ProjectContributeSchema,
                                 current_user: UserSchema = Depends(get_current_active_user)):

        project: ProjectResponseSchema = service_locator.general_service.get_data_by_id(
            db=self.db, key=id, model=Project)

        if project.deadline < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot contribute after the deadline"
            )

        data = data.model_dump(exclude_unset=True)
        contribution_amount = Decimal(data.get('contribution_amount'))

        total_contribution = service_locator.project_service.get_total_contributions(
            self.db, project.id)

        remaining_contribution = Decimal(
            project.goal_amount) - Decimal(total_contribution)

        if remaining_contribution <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Contribution goal has already been reached. No further contributions are allowed."
            )

        if contribution_amount > remaining_contribution:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Contribution exceeds the project's goal amount. \
                    You can only contribute up to {:.2f} more.".format(remaining_contribution)
            )

        service_locator.project_service.add_contribution(
            db=self.db, user_id=current_user.id, project_id=project.id, amount=contribution_amount)

        self.add_project_additional_data(project)

        return project

    @router.delete("/{id}/")
    async def delete_project(self, id: UUID4):
        project = service_locator.general_service.delete_data(
            self.db, id, Project)
        return project

    @router.put("/{id}/", response_model=ProjectResponseSchema)
    @router.patch("/{id}/", response_model=ProjectResponseSchema)
    async def update_project(self, id: UUID4, data: ProjectCreateSchema):
        data = data.model_dump(exclude_unset=True)

        updated_project = service_locator.general_service.update_data(
            db=self.db,
            key=id,
            data=data,
            model=Project,
        )
        self.add_project_additional_data(updated_project)
        return updated_project


add_pagination(router)
