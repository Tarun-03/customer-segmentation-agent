# from fastapi import FastAPI

# from .routes import router

# app = FastAPI(
#     title="Customer Segmentation API",
#     version="1.0.0"
# )

# app.include_router(router)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import router

app = FastAPI(title="Customer Segmentation API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # fine for a hackathon demo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)