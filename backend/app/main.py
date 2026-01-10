from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from .routes.upload import router as upload_router
from .routes.convert import router as convert_router


BASE_DIR = Path(__file__).resolve().parent

OUTPUT_DIR = BASE_DIR / "uploads" / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="Custom Handwriting Converter")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router, prefix="/api")
app.include_router(convert_router, prefix="/api")

# ✅ Serve images from backend/app/uploads/output
app.mount(
    "/outputs",
    StaticFiles(directory=OUTPUT_DIR),
    name="outputs"
)

@app.get("/")
def root():
    return {"message": "Backend is running"}
