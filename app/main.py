import sys
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import app.settings.base
from app.api import miners, files
from apscheduler.schedulers.background import BackgroundScheduler
from app.utils.pull_data import get_runs_dataframe
from app.utils.model_conversion import convert_models_to_onnx
from app.settings.config import MEDIA_DIR
from contextlib import asynccontextmanager


def my_scheduled_task():
    try:
        if get_runs_dataframe():
            convert_models_to_onnx(
                json_file=f"{MEDIA_DIR}/table/miners.json",
                nsga_net_path="./nsga-net",
                logs_path="./logs",
                files_path=f"{MEDIA_DIR}/files",
            )
            print("Running scheduled task... Data retrieved.")
    except Exception as e:
        print(f"Error fetching data: {e}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        my_scheduled_task, "interval", minutes=0.1
    )  # Task every minute
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
