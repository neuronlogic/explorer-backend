import wandb
import os
import json
import pandas as pd
import sys

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
)
from app.settings.config import MEDIA_DIR, ROOT_DIR


# Load environment variables from .env file
def initialize_wandb(api_key: str) -> None:
    """Initialize wandb with the provided API key."""
    try:
        wandb.login(key=api_key)
    except Exception as e:
        raise e


def load_config(config_path: str) -> dict:
    """Load configuration from a JSON file."""
    try:
        with open(config_path, "r") as file:
            config = json.load(file)
        return config
    except Exception as e:
        raise e


def load_most_recent_times(filepath: str) -> dict:
    """Load most_recent_times from a JSON file."""
    try:
        if os.path.exists(filepath):
            with open(filepath, "w") as f:
                return json.load(f)
        else:
            return {}
    except Exception as e:
        raise e


def save_most_recent_times(filepath: str, most_recent_times: dict) -> None:
    """Save most_recent_times to a JSON file."""
    try:
        with open(filepath, "w") as f:
            json.dump(most_recent_times, f)
    except Exception as e:
        raise e


def get_runs_dataframe():
    try:
        print("getting runs dataframe")
        config = load_config(f"{ROOT_DIR}/settings/validators.json")

        entity = config.get("entity")
        project = config.get("project")
        run_ids = config.get("run_ids")
        wandb_api_key = os.getenv("WANDB_API_KEY")
        initialize_wandb(wandb_api_key)
        api = wandb.Api()

        most_recent_times_filepath = (
            f"{MEDIA_DIR}/table/most_recent_times.json"
        )
        most_recent_times = load_most_recent_times(most_recent_times_filepath)

        for run_id_item in run_ids:
            run_id = run_id_item["id"]
            run_id_value = run_id_item["value"]
            run = api.run(f"{entity}/{project}/{run_id_value}")

            saved_run_time = most_recent_times.get(run_id, None)

            most_recent_file = None
            most_recent_time = None

            # Iterate through files and find the most recent one in /Files/media/table
            for file in run.files():
                if file.name.startswith("media/table"):
                    # Update most recent file if necessary
                    if saved_run_time and file.updated_at <= saved_run_time:
                        continue

                    # Update the most recent file if necessary
                    if (
                        most_recent_time is None
                        or file.updated_at > most_recent_time
                    ):
                        most_recent_file = file
                        most_recent_time = file.updated_at

            if most_recent_file:
                file_path = most_recent_file.download(replace=True)

                custom_filename = f"{MEDIA_DIR}/table/validator{run_id}.json"

                # Rename the downloaded file to the custom filename
                os.rename(file_path.name, custom_filename)

                most_recent_times[run_id] = most_recent_time

                with open(custom_filename, "r") as f:
                    table = json.load(f)
                    columns = table["columns"]
                    data = table["data"]
                    pd.DataFrame(data, columns=columns)

        save_most_recent_times(most_recent_times_filepath, most_recent_times)

        print(most_recent_times)
        return True
    except Exception as e:
        raise e
