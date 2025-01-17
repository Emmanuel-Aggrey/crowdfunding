from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
import requests
from contextlib import asynccontextmanager
from app.settings import BASE_URL
import logging
scheduler = BackgroundScheduler()


def ping_render():
    if BASE_URL:
        try:
            response = requests.get(BASE_URL)
            logging.info("Pinged {}, Status Code: {}".format(
                BASE_URL, response.status_code))
        except requests.RequestException as e:
            logging.error(f"Error pinging {BASE_URL}: {e}")
    else:
        logging.warning("BASE_URL is not set!")


scheduler.add_job(ping_render, 'interval', minutes=14)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("FastAPI app started. Scheduler is running.")
    scheduler.start()

    yield

    logging.info("Shutting down FastAPI app. Stopping scheduler.")
    scheduler.shutdown()
