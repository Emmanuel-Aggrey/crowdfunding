
from app.models import Contribution
from sqlalchemy import func
from app.project.models import Project
from pydantic import UUID4
from sqlalchemy.orm import Session
from app.accounts.models import User
from sqlalchemy.exc import SQLAlchemyError
from app.accounts.schemas import UserResponseSchema
import logging


class ProjectService:

    def get_total_contributions(self, db: Session, project_id: UUID4) -> float:
        total_contributions = (
            db.query(func.sum(Contribution.amount))
            .filter(Contribution.project_id == project_id)
            .scalar()
        )
        return total_contributions or 0.0

    def add_contribution(self, db: Session, user_id: UUID4, project_id: UUID4, amount: float) -> bool:
        from app.core.dependency_injection import service_locator

        try:

            user = service_locator.general_service.get_data_by_id(
                db=db, key=user_id, model=User)

            service_locator.general_service.raise_not_found(
                user, f'user {user_id} not found')

            project = service_locator.general_service.get_data_by_id(
                db=db, key=project_id, model=Project)

            service_locator.general_service.raise_not_found(
                project, f'project {project_id} not found')

            contribution = Contribution(
                amount=amount,
                user_id=user_id,
                project_id=project_id
            )

            db.add(contribution)
            db.commit()

            return True

        except SQLAlchemyError as e:
            db.rollback()
            logging.error(f"Error adding contribution: {str(e)}")
            return False

    def get_contributors(self, db: Session, project_id: UUID4):

        contributors_query = (
            db.query(User)
            .join(Contribution, Contribution.user_id == User.id)
            .filter(Contribution.project_id == project_id)
            .distinct()
            .all()
        )

        return [UserResponseSchema.model_validate(contributor) for contributor in contributors_query]
