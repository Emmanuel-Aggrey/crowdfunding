import os
import subprocess
import pytest
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

from app.database import Base
from app.models import User, Project  # noqa
from app.test.base import engine


# Load environment variables from .env file
load_dotenv()

# This fixture will set up the test database before tests and tear it down after


@pytest.fixture(scope='session')
def setup_database():
    # Set the environment to testing
    os.environ["IS_TESTING"] = "True"
    is_ci = os.getenv("IS_CI") == "True"

    # Set the database name for testing
    test_database_name = "test_" + os.getenv("DATABASE_NAME")
    os.environ["DATABASE_NAME"] = test_database_name

    # Create the test database (it will be dropped and recreated)
    create_database(test_database_name, os.getenv(
        "DATABASE_USER"), os.getenv("DATABASE_PASSWORD"))

    # Drop all existing tables (if any) and recreate them
    print("Creating tables and applying migrations...")
    Base.metadata.drop_all(bind=engine)
    subprocess.run(["alembic", "upgrade", "head"], check=True)

    # Set up a sessionmaker to interact with the database
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = Session()

    yield session  # This will be passed to the test

    # Tear down: Close the session after the test finishes
    session.close()

    # Optionally, drop the test database after tests are done (if needed)
    # if not is_ci:
    # print("Dropping test database...")
    (test_database_name, os.getenv(
        "DATABASE_USER"), os.getenv("DATABASE_PASSWORD"))


# Helper function to create a new database
def create_database(database_name, user_name, password):
    import psycopg2
    from psycopg2 import sql
    from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

    con = psycopg2.connect(
        dbname="postgres", user=user_name, host="", password=password
    )

    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    cur = con.cursor()

    # Drop the test database if it exists and create a new one
    cur.execute(
        sql.SQL("DROP DATABASE IF EXISTS {}").format(
            sql.Identifier(database_name))
    )
    cur.execute(sql.SQL("CREATE DATABASE {}").format(
        sql.Identifier(database_name)))

    # Close the connection
    cur.close()
    con.close()


# Helper function to drop the database after testing (optional)
def drop_database(database_name, user_name, password):
    import psycopg2
    from psycopg2 import sql
    from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

    con = psycopg2.connect(
        dbname="postgres", user=user_name, host="", password=password
    )

    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    cur = con.cursor()

    # Drop the test database
    cur.execute(
        sql.SQL("DROP DATABASE IF EXISTS {}").format(
            sql.Identifier(database_name))
    )

    # Close the connection
    cur.close()
    con.close()
