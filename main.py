from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.router.download import router as download_router

app = FastAPI(
    title="SnapTik Clone API",
    version="1.0.0",
    description="API download video TikTok không watermark"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(download_router)

@app.get("/")
def home():
    return {"message": "SnapTik API is running!"}
