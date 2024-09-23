import wandb
import os
import json
import pandas as pd
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the WANDB API key from environment variable
wandb_api_key = os.getenv('WANDB_API_KEY')

# Log in to Weights and Biases using the API key
wandb.login(key=wandb_api_key)

# Define the project and run you want to download files from
entity = os.getenv('ENTITY')  # Replace with your wandb entity
project = os.getenv('PROJECT') # Replace with your wandb project
run_id = os.getenv('RUN_ID')  # Replace with your run ID


def get_runs_dataframe(run_id):
    api = wandb.Api()

    # Get the run
    run = api.run(f"{entity}/{project}/{run_id}")

    most_recent_file = None
    most_recent_time = None

    # Iterate through files and find the most recent one in /Files/media/table
    for file in run.files():
        if file.name.startswith("media/table"):
            # Update most recent file if necessary
            if most_recent_time is None or file.updated_at > most_recent_time:
                most_recent_file = file
                most_recent_time = file.updated_at

    custom_filename = "media/table/miners.json"
    file_path = most_recent_file.download(replace=True)
    
    # Rename the downloaded file to the custom filename
    os.rename(file_path.name, custom_filename)

    # Load the downloaded file as JSON using the new custom filename
    with open(custom_filename, 'r') as f:
        table = json.load(f)
        columns = table['columns']
        data = table['data']
        df = pd.DataFrame(data, columns=columns)

    # If everything is successful, return True
    return True


def get_pareto_rows(df, col):
    df_sorted = df.sort_values(by=col)

    pareto_frontier = []
    max_accuracy = -float('inf')

    for index, row in df_sorted.iterrows():
        if row['accuracy'] > max_accuracy:
            pareto_frontier.append(index)
            max_accuracy = row['accuracy']

    return df.loc[pareto_frontier]
