import json
import pandas as pd
from pathlib import Path


def get_miners(json_file):
    try:
        if not Path(json_file).exists():
            return None

        with open(json_file, "r") as f:
            json_data = json.load(f)

        df = pd.DataFrame(json_data["data"], columns=json_data["columns"])

        miners_data = df[
            [
                "uid",
                "hf_account",
                "params",
                "flops",
                "accuracy",
                "pareto",
                "reward",
                "commit",
                "eval_date",
                "score",
                "block",
            ]
        ]
        return miners_data.to_dict(orient="records")

    except Exception as e:
        print(f"Error loading miners data: {str(e)}")
        return None
