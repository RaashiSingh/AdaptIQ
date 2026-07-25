from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
import aiofiles
import os
from app.rag.pipeline import process_uploaded_file

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = [".pdf", ".docx", ".txt"]

processing_status = {}

def process_in_background(filename: str, user_id: str):
    try:
        processing_status[filename] = "processing"
        result = process_uploaded_file(filename, user_id)
        processing_status[filename] = f"done:{result['chunks_stored']} chunks"
        print(f"[Upload] Done processing {filename}")
    except Exception as e:
        processing_status[filename] = f"error:{str(e)}"
        print(f"[Upload] Error processing {filename}: {e}")

@router.post("/")
async def upload_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    user_id: str = "default_user"
):
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

    background_tasks.add_task(process_in_background, file.filename, user_id)
    processing_status[file.filename] = "queued"

    return {
        "filename": file.filename,
        "size_bytes": len(content),
        "message": "File uploaded. Processing in background...",
        "status": "queued"
    }

@router.get("/status/{filename}")
def get_processing_status(filename: str):
    status = processing_status.get(filename, "unknown")
    return {"filename": filename, "status": status}

@router.get("/list")
def list_uploads():
    files = os.listdir(UPLOAD_DIR)
    return {"files": files}