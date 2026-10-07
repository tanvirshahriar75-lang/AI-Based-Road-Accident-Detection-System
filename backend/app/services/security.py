from pathlib import Path
import re

SAFE_FILENAME = re.compile(r"[^A-Za-z0-9._-]+")

def safe_filename(filename: str) -> str:
    name = Path(filename).name
    name = SAFE_FILENAME.sub("_", name).strip("._")
    return name or "uploaded_video"
