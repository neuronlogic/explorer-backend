from fastapi import APIRouter, HTTPException
from app.models.miners import get_miners
from app.settings.config import MEDIA_DIR

router = APIRouter()


@router.get("/get-miners/{validator_id}")
def serve_miners(validator_id: int, status: str = "current"):
    if status not in ["current", "archived"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid status. Must be 'current' or 'archived'",
        )

    # Adjust path based on status
    status_path = "archived" if status == "archived" else "current"
    file_path = f"{MEDIA_DIR}/{status_path}/table/validator{validator_id}.json"

    miners_list = get_miners(file_path)

    print(miners_list)
    if not miners_list:
        raise HTTPException(status_code=404, detail="Miners data not found")
    return miners_list
