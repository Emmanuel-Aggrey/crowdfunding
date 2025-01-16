
from app.core.models import BaseModel as Model
from fastapi import HTTPException
from fastapi import status
from pydantic import BaseModel
from pydantic import UUID4
from sqlalchemy.orm import Session


class GeneralService:
    def create_data(self, db: Session, model: BaseModel) -> Model:
        db.add(model)
        db.commit()
        db.refresh(model)

        return model

    def list_data(self, db: Session, model: BaseModel):
        return db.query(model).all()

    def filter_data(
        self,
        db: Session,
        filter_values: dict,
        model: BaseModel,
        single_record: bool = False,
    ):
        query = db.query(model)

        for key, value in filter_values.items():
            if hasattr(model, key):
                query = query.filter(getattr(model, key) == value)

        return query.one_or_none() if single_record else query.all()

    def get_data_by_id(self, db: Session, key: UUID4, model: BaseModel):
        data = db.query(model).filter(model.id == key).one_or_none()

        self.raise_not_found(data)
        return data

    def delete_data(self, db: Session, key: UUID4, model: BaseModel, **kwargs: dict):
        data = db.query(model).filter(model.id == key).first()

        self.raise_not_found(data)
        db.delete(data)
        db.commit()

        return

    def update_data(
        self, db: Session, key: UUID4, data: dict, model: BaseModel
    ) -> Model:
        project = db.query(model).filter(model.id == key).first()
        self.raise_not_found(project)

        for key, value in data.items():
            if hasattr(project, key):
                setattr(project, key, value)

        db.commit()
        db.refresh(project)

        return project

    def raise_not_found(self, model: BaseModel, message=None):
        if model is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{status.HTTP_404_NOT_FOUND} {message}",
            )
        return
