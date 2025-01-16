# SET UP

1. Create a virtual environment (python3.12+)
2. `$ pip install -r requirements.txt`
3. `$ pre-commit install`
4. create .env file
5. copy .env.example to .env and update the values
6. `$ alembic upgrade head`
7. `$ fastapi dev`

# Init Alembic

```bash
$ alembic init migrations
```

# Creating migration

```bash
$ alembic revision --autogenerate -m "first migrations"
$ alembic upgrade head

# To downgrade
$ alembic downgrade -1

```

# RUN TEST

```bash
$ pytest -v app or pytest -v app/module
or
$ fastapi dev  --reload --host 0.0.0.0 --port 8002
```
