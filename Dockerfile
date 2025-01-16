FROM python:3.12-slim


RUN apt-get update && \
    apt-get install -y libpq-dev build-essential postgresql-client

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x scripts/start.sh

EXPOSE 8005

CMD ["scripts/start.sh"]
