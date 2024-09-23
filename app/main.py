import os
import json
from pathlib import Path
from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from apscheduler.schedulers.background import BackgroundScheduler
from pull_data import get_runs_dataframe  # Updated import path to match the file structure
from model_conversion import convert_models_to_onnx

# Load environment variables
os.environ['TZ'] = 'Etc/UTC'
run_id = os.getenv('RUN_ID')  # Ensure that RUN_ID is fetched from the environment

app = FastAPI()

# Define the directory where ONNX files are stored
MEDIA_DIR  = Path(__file__).parent / 'media'
FILE_DIR = MEDIA_DIR / 'files'
scheduler = BackgroundScheduler()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)


def my_scheduled_task():
    if run_id:
        try:
            if get_runs_dataframe(run_id):
                convert_models_to_onnx(json_file=f"{MEDIA_DIR}/table/miners.json", nsga_net_path="./nsga-net", logs_path="./logs",files_path=f"{MEDIA_DIR}/files")
            print("Running scheduled task... Data retrieved.")
        except Exception as e:
            print(f"Error fetching data: {e}")
    else:
        print("RUN_ID not found in environment variables.")


@app.on_event("startup")
def start_scheduler():
    # Run the task once immediately when the server starts
    my_scheduled_task()

    # Schedule the task to run at regular intervals
    scheduler.add_job(my_scheduled_task, 'interval', hours=2)
    scheduler.start()
    print("Scheduler started.")


@app.on_event("shutdown")
def shutdown_scheduler():
    scheduler.shutdown()
    print("Scheduler shut down.")


def get_miners(json_file):
    try:
        # Check if the file exists
        if not Path(json_file).exists():
            print(f"Error: The file '{json_file}' does not exist.")
            return None

        # Try to open and load the JSON file
        with open(json_file, 'r') as f:
            json_data = json.load(f)

        # Convert JSON data to DataFrame
        df = pd.DataFrame(json_data['data'], columns=json_data['columns'])

        # Extract specific columns
        miners_data = df[['uid', 'hf_account', 'params', 'flops', 'accuracy',
                          'pareto', 'reward', 'commit', 'eval_date', 'score', 'block']]

        # Convert DataFrame to a list of dictionaries
        miners_list = miners_data.to_dict(orient='records')
        return miners_list

    except FileNotFoundError:
        print(f"Error: The file '{json_file}' could not be found.")
    except json.JSONDecodeError:
        print(f"Error: The file '{json_file}' contains invalid JSON.")
    except KeyError as e:
        print(f"Error: Missing expected column in data - {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return None

# Serve ONNX files from the '/onnx' route
@app.get("/files/{uid}")
def serve_onnx_file(uid: str):
    # Construct the file path
    file_path = FILE_DIR / uid

    # Check if the file exists
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="<html><body><h1>File not found</h1></body></html>", headers={"Content-Type": "text/html"})

    # Read the ONNX file content
    try:
        with open(file_path, "rb") as file:
            content = file.read()
        return Response(content, media_type="application/octet-stream")
    except Exception as e:
        error_message = f"<html><body><h1>Error reading file: {str(e)}</h1></body></html>"
        raise HTTPException(status_code=500, detail=error_message, headers={"Content-Type": "text/html"})

@app.get("/get-miners")
def serve_miners():
    miners_list = get_miners(f'{MEDIA_DIR}/table/miners.json')
    return miners_list

@app.get("/")
def read_root():
    return {"message": "Welcome to the ONNX file server"}
