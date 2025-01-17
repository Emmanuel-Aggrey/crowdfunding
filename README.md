# SET UP

1. Create a virtual environment (python3.12+)
2. `$ pip install -r requirements.txt`
3. `$ pre-commit install`
4. create .env file
5. copy .env.example to .env and update the values
6. `$ alembic upgrade head`
7. `$ fastapi dev ` or `$ fastapi dev --host 0.0.0.0 --port 8005`
8. `$ http://127.0.0.1:8000/docs`

# Init Alembic

```bash
$ alembic init migrations
$ alembic revision --autogenerate -m "first migrations"
```

# To downgrade

```bash

$ alembic downgrade -1

```

# RUN TEST

```bash
$ pytest -v app or pytest -v app/module

```

# Spin up with Docker

```bash
$ docker pull aggrey/crowdfunding-app:latest
# setup environment variables as shown above
$ docker-compose build
$ docker-compose up
visit http://127.0.0.1:8005/docs#/


```
