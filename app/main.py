from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import upload, chat

app = FastAPI(title="MIA Backend API", description="Medical Image Analysis Backend MVP")

# Configure CORS to allow Expo app to communicate with this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For dev only. In production, restrict to frontend domain.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(upload.router, prefix="/api/upload", tags=["Upload"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])

@app.get("/")
def read_root():
    return {"status": "ok", "message": "MIA Backend MVP is running."}
