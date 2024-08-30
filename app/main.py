from fastapi import FastAPI, HTTPException, Response
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Define the directory where ONNX files are stored
FILE_DIR = Path(__file__).parent / 'files'

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Serve ONNX files from the '/onnx' route
@app.get("/files/{uid}")
def serve_onnx_file(uid: str):
    # Construct the file path
    file_path = FILE_DIR / uid

    print(file_path)
    # Check if the file exists
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="<html><body><h1>File not found</h1></body></html>", headers={"Content-Type": "text/html"})

    # Read the ONNX file content
    try:
        with open(file_path, "rb") as file:
            content = file.read()
        return Response(content, media_type="application/octet-stream")
    except Exception as e:
        error_message = f"<html><body><h1>Error reading file: {str(e)}</h1></body></html>"
        raise HTTPException(status_code=500, detail=error_message, headers={"Content-Type": "text/html"})

@app.get("/")
def read_root():
    return {"message": "Welcome to the ONNX file server"}
