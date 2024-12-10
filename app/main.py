import sys
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import app.settings.base
from app.api import miners, files, validators
from apscheduler.schedulers.background import BackgroundScheduler
from app.utils.process_validator import process_validator_data
from contextlib import asynccontextmanager


def scheduled_task():
    try:
        process_validator_data(status="current")

        print("Running scheduled task... Data retrieved.")
    except Exception as e:
        print(f"Error fetching data: {e}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting scheduler...")

    scheduler = BackgroundScheduler()
    scheduler.add_job(scheduled_task, "interval", hours=1)  # Task every minute
    scheduler.start()
    print("Scheduler started.")

    yield

    scheduler.shutdown()
    print("Scheduler shut down.")


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

app.include_router(miners.router)
app.include_router(files.router)
app.include_router(validators.router)
