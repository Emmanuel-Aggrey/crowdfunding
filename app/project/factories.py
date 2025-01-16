

import factory.random
from app.project.models import Project
from app.test.base import BaseTest
from datetime import datetime, timedelta
from decimal import Decimal


class ProjectFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Project
        sqlalchemy_session = BaseTest.get_db()
        sqlalchemy_session_persistence = "commit"

    title = factory.Faker("name")
    description = factory.Faker("text")
    goal_amount = factory.LazyFunction(lambda: Decimal("1000.00"))
    deadline = factory.LazyFunction(
        lambda: datetime.utcnow() + timedelta(days=30))
