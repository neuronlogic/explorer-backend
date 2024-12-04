import json
from pathlib import Path


def get_validators(json_file):
    try:
        if not Path(json_file).exists():
            return None

        with open(json_file, "r") as f:
            json_data = json.load(f)

        return json_data["run_ids"]

    except Exception as e:
        print(f"Error loading miners data: {str(e)}")
        return None
