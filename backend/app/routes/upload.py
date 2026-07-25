from fastapi import APIRouter, UploadFile, File, HTTPException
import aiofiles
import os

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = [".pdf", ".docx", ".txt"]

@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File type {ext} not allowed. Use PDF, DOCX, or TXT."
        )

    save_path = os.path.join(UPLOAD_DIR, file.filename)
    async with aiofiles.open(save_path, "wb") as f:
        content = await file.read()
        await f.write(content)

    return {
        "filename": file.filename,
        "size": len(content),
        "message": "File uploaded successfully. Ready for processing."
    }

@router.get("/list")
def list_uploads():
    files = os.listdir(UPLOAD_DIR)
    return {"files": files}