import factory
from app.test.base import BaseTest

from .models import User


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = BaseTest.get_db()
        sqlalchemy_session_persistence = "commit"

    is_active = True
    email = factory.Faker("email")
    hashed_password = factory.Faker("name")
    username = factory.Faker("name")
