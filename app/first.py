import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.utils.model_conversion import convert_models_to_onnx
from app.utils.pull_data import load_config
from app.settings.config import ROOT_DIR, MEDIA_DIR


def my_scheduled_task():
    try:
        config = load_config(f"{ROOT_DIR}/settings/validators.json")
        json_files = [
            f"{MEDIA_DIR}/table/validator{validator['id']}.json"
            for validator in config.get("run_ids")
        ]
        convert_models_to_onnx(
            json_files=json_files,
            nsga_net_path=f"{ROOT_DIR}/nsga-net",
            logs_path=f"{ROOT_DIR}/logs",
            files_path=f"{MEDIA_DIR}/files",
        )
        print("Running scheduled task... Data retrieved.")
    except Exception as e:
        print(f"Error fetching data: {e}")


my_scheduled_task()
