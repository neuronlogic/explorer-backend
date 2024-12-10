from typing import Dict
from pathlib import Path

from app.utils.pull_data import get_runs_dataframe
from app.utils.model_conversion import convert_models_to_onnx
from app.settings.config import ROOT_DIR, MEDIA_DIR


def process_validator_data(validator_config: Dict, status: str) -> None:
    """
    Process validator data and convert models to ONNX format.

    Args:
        validator_config: Dictionary containing validator configuration
        status: Status of the validator ('archived' or 'current')
    """
    if not get_runs_dataframe(status=status):
        return

    run_ids = validator_config.get("run_ids", [])
    base_path = f"{MEDIA_DIR}/{status}"

    json_files = [
        Path(base_path) / "table" / f"validator{validator['id']}.json"
        for validator in run_ids
    ]

    convert_models_to_onnx(
        json_files=json_files,
        nsga_net_path=Path(ROOT_DIR) / "nsga-net",
        logs_path=Path(ROOT_DIR) / "logs",
        files_path=Path(base_path) / "files",
    )
