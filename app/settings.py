import os

from dotenv import dotenv_values

# Load environment variables from .env file

config = {
    **dotenv_values(".env"),  # load sensitive variables
    **os.environ,  # override loaded values with environment variables
}


SECRET_KEY = config.get("SECRET_KEY")
ALGORITHM = config.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE = int(config.get("ACCESS_TOKEN_EXPIRE"))
BASE_URL = config.get("BASE_URL")

DATABASE_HOST = config.get("DATABASE_HOST")
DATABASE_USER = config.get("DATABASE_USER")
DATABASE_PASSWORD = config.get("DATABASE_PASSWORD")
DATABASE_NAME = config.get("DATABASE_NAME")
DATABASE_PORT = config.get("DATABASE_PORT")

IS_TESTING = config.get("IS_TESTING") == "True"
DEBUG = config.get("DEBUG", "False") == "True"


SQLALCHEMY_DATABASE_URL = (
    "postgresql://{user}:{password}@{host}:{port}/{dbname}".format(
        user=DATABASE_USER,
        password=DATABASE_PASSWORD,
        host=DATABASE_HOST,
        port=DATABASE_PORT,
        dbname=DATABASE_NAME,
    )
)
