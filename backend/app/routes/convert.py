from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pathlib import Path
import uuid

from app.services.extractor import extract_text
from app.services.renderer import render_handwritten_text
from app.services.fonts import FONT_MAP

router = APIRouter()

# ✅ BASE DIRECTORY (backend/app → backend)
BASE_DIR = Path(__file__).resolve().parent.parent

# ✅ ABSOLUTE, SAFE PATHS
UPLOAD_DIR = BASE_DIR / "uploads" / "input"
OUTPUT_DIR = BASE_DIR / "uploads" / "output"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

BACKGROUND_PATH = BASE_DIR / "assets" / "backgrounds" / "notebook.jpg"



class ConvertRequest(BaseModel):
    file_id: str
    file_type: str  # "text" or "handwritten"
    font_key: str | None = "handwriting"
    



@router.post("/convert")
def convert_file(data: ConvertRequest):
    if data.file_type != "text":
        raise HTTPException(
            status_code=400,
            detail="Only text conversion supported for now"
        )

    input_file = UPLOAD_DIR / f"{data.file_id}.txt"

    if not input_file.exists():
        raise HTTPException(status_code=404, detail="Input file not found")

    # 1️⃣ Extract text
    extracted_text = extract_text(input_file, data.file_type)

    if not extracted_text.strip():
        raise HTTPException(status_code=400, detail="Extracted text is empty")

    # 2️⃣ Resolve font
    font_path = FONT_MAP.get(data.font_key)
    if not font_path:
        raise HTTPException(status_code=400, detail="Invalid font selected")

    # 3️⃣ Render handwritten image
    output_id = str(uuid.uuid4())
    output_path = OUTPUT_DIR / f"{output_id}.png"

    render_handwritten_text(
    text=extracted_text,
    output_path=output_path,
    font_path=Path(font_path),
    background_path=BACKGROUND_PATH,
)


    return {
        "status": "ok",
        "output_id": output_id,
        "output_path": str(output_path)
    }
