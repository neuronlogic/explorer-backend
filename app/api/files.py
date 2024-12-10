from fastapi import APIRouter, HTTPException, Response
from app.settings.config import MEDIA_DIR

router = APIRouter()


@router.get("/files/{uid}")
def serve_onnx_file(uid: str, status: str = "current"):
    # Validate status
    if status not in ["current", "archived"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid status. Must be 'current' or 'archived'",
        )

    # Adjust file path based on status
    base_path = (
        MEDIA_DIR
        / ("archived" if status == "archived" else "current")
        / "files"
    )
    file_path = base_path / uid

    print(file_path)
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")

    try:
        with open(file_path, "rb") as file:
            content = file.read()
        return Response(content, media_type="application/octet-stream")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error reading file: {str(e)}"
        )
