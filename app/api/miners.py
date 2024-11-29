from fastapi import APIRouter, HTTPException
from app.models.miners import get_miners
from app.settings.config import MEDIA_DIR

router = APIRouter()


@router.get("/get-miners")
def serve_miners():
    miners_list = get_miners(f"{MEDIA_DIR}/table/miners.json")
    if not miners_list:
        raise HTTPException(status_code=404, detail="Miners data not found")
    return miners_list
