from typing import List, Dict, Any
from pydantic import BaseModel, Field


# -----------------------------
# Chat Models
# -----------------------------

class ChatRequest(BaseModel):

    query: str = Field(
        ...,
        example="Find high value customers with low engagement"
    )


class ChatResponse(BaseModel):

    response: str
    execution_plan: List[str]
    results: Dict[str, Any]


# -----------------------------
# Upload Models
# -----------------------------

class UploadResponse(BaseModel):

    filename: str
    rows: int
    columns: int
    message: str


# -----------------------------
# Segmentation Models
# -----------------------------

class SegmentResponse(BaseModel):

    segments: List[Dict[str, Any]]


# -----------------------------
# Persona Models
# -----------------------------

class PersonaResponse(BaseModel):

    personas: List[Dict[str, Any]]


# -----------------------------
# Recommendation Models
# -----------------------------

class RecommendationResponse(BaseModel):

    recommendations: List[Dict[str, Any]]


# -----------------------------
# Chart Models
# -----------------------------

class ChartsResponse(BaseModel):

    charts: Dict[str, Any]