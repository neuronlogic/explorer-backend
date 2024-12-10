import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.utils.process_validator import process_validator_data


def scheduled_task() -> None:
    """Execute the scheduled task for processing validator data."""
    try:
        process_validator_data("archived")
        process_validator_data("current")

    except Exception:
        raise


if __name__ == "__main__":
    scheduled_task()
