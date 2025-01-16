import os

from dotenv import dotenv_values

# Load environment variables from .env file

config = {
    **dotenv_values(".env"),  # load sensitive variables
    **os.environ,  # override loaded values with environment variables
}


SECRET_KEY = config.get("SECRET_KEY")
ALGORITHM = config.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(config.get("ACCESS_TOKEN_EXPIRE_MINUTES"))
ORGANISATION_TOKEN_EXPIRE_DAYS = int(
    config.get("ORGANISATION_TOKEN_EXPIRE_DAYS"))


DATABASE_HOST = config.get("DATABASE_HOST")
DATABASE_USER = config.get("DATABASE_USER")
DATABASE_PASSWORD = config.get("DATABASE_PASSWORD")
DATABASE_NAME = config.get("DATABASE_NAME")
DATABASE_PORT = config.get("DATABASE_PORT")
SENTRY_DSN = config.get("SENTRY_DSN")
CHAT_API_BASE_URL = config.get("CHAT_API_BASE_URL")

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


AWS_S3_REGION_NAME = config.get("AWS_S3_REGION_NAME")
AWS_SECRET_ACCESS_KEY = config.get("AWS_SECRET_ACCESS_KEY")
AWS_ACCESS_KEY_ID = config.get("AWS_ACCESS_KEY_ID")
BUCKET_NAME = config.get("AWS_STORAGE_BUCKET_NAME")
AWS_PRESIGNED_EXPIRY = int(config.get("AWS_PRESIGNED_EXPIRY"))
FILE_MAX_SIZE = int(config.get("FILE_MAX_SIZE"))
AWS_DEFAULT_ACL = "public-read"
