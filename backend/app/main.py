from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import auth, chat, upload, progress

app = FastAPI(
    title="AdaptIQ API",
    description="Personalized AI Tutor Backend",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router,     prefix="/api/auth",     tags=["Authentication"])
app.include_router(chat.router,     prefix="/api/chat",     tags=["Chat"])
app.include_router(upload.router,   prefix="/api/upload",   tags=["Upload"])
app.include_router(progress.router, prefix="/api/progress", tags=["Progress"])

@app.get("/")
def root():
    return {"message": "AdaptIQ API is running!", "docs": "/docs"}

@app.get("/health")
def health():
    return {"status": "healthy"}