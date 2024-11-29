# app/config.py
from pathlib import Path

# Define the directory where ONNX files are stored
ROOT_DIR = Path(__file__).parent.parent
MEDIA_DIR = ROOT_DIR / "media"
FILE_DIR = MEDIA_DIR / "files"
