from fastapi import APIRouter, HTTPException
from app.models.miners import get_miners
from app.settings.config import MEDIA_DIR

router = APIRouter()


@router.get("/get-miners/{validator_id}")
def serve_miners(validator_id: int):
    miners_list = get_miners(f"{MEDIA_DIR}/table/validator{validator_id}.json")
    if not miners_list:
        raise HTTPException(status_code=404, detail="Miners data not found")
    return miners_list
