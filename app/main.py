from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import router

app = FastAPI(
    title="Customer Segmentation Agent",
    description="AI-powered Retail Banking Customer Segmentation Agent",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register Routes
app.include_router(router)


@app.get("/", tags=["Health"])
def home():
    return {
        "message": "Customer Segmentation Agent API is running!"
    }