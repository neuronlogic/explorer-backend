from fastapi import APIRouter, HTTPException
from app.models.validators import get_validators
from app.settings.config import ROOT_DIR

router = APIRouter()


@router.get("/get-validator")
def serve_validators():
    validators_list = get_validators(f"{ROOT_DIR}/settings/validators.json")
    if not validators_list:
        raise HTTPException(status_code=404, detail="Miners data not found")
    return validators_list
