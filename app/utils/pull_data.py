import wandb
import os
import json
import pandas as pd
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


def get_runs_dataframe():
    try:
        config = load_config(f"{ROOT_DIR}/settings/validators.json")
        entity = config.get("entity")
        project = config.get("project")
        run_id = config.get("run_id")
        print(f"{entity}/{project}/{run_id[0]['value']}")
        wandb_api_key = os.getenv("WANDB_API_KEY")
        initialize_wandb(wandb_api_key)
        api = wandb.Api()

        run = api.run(f"{entity}/{project}/{run_id[0]['value']}")

        most_recent_file = None
        most_recent_time = None

        # Iterate through files and find the most recent one in /Files/media/table
        for file in run.files():
            if file.name.startswith("media/table"):
                # Update most recent file if necessary
                if (
                    most_recent_time is None
                    or file.updated_at > most_recent_time
                ):
                    most_recent_file = file
                    most_recent_time = file.updated_at

        custom_filename = f"{MEDIA_DIR}/table/miners.json"
        file_path = most_recent_file.download(replace=True)

        # Rename the downloaded file to the custom filename
        os.rename(file_path.name, custom_filename)

        # Load the downloaded file as JSON using the new custom filename
        with open(custom_filename, "r") as f:
            table = json.load(f)
            columns = table["columns"]
            data = table["data"]
            pd.DataFrame(data, columns=columns)

        # If everything is successful, return True
        return True
    except Exception as e:
        raise e


# def get_pareto_rows(df, col):
#     df_sorted = df.sort_values(by=col)

#     pareto_frontier = []
#     max_accuracy = -float("inf")

#     for index, row in df_sorted.iterrows():
#         if row["accuracy"] > max_accuracy:
#             pareto_frontier.append(index)
#             max_accuracy = row["accuracy"]

#     return df.loc[pareto_frontier]

get_runs_dataframe()
