from fastapi import APIRouter, HTTPException
from app.models.validators import get_validators
from app.settings.config import ROOT_DIR

router = APIRouter()


@router.get("/get-validator")
def serve_validators(status: str = "current"):
    if status not in ["current", "archived"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid status. Must be 'current' or 'archived'",
        )

    # Adjust path based on status
    status_path = "archived" if status == "archived" else "current"
    file_path = f"{ROOT_DIR}/settings/{status_path}/validators.json"

    validators_list = get_validators(file_path)
    if not validators_list:
        raise HTTPException(status_code=404, detail="Miners data not found")
    return validators_list
