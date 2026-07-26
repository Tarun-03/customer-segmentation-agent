from fastapi import APIRouter, UploadFile, File, HTTPException, status

from app.schemas import (
    ChatRequest,
    ChatResponse,
    UploadResponse,
    SegmentResponse,
    PersonaResponse,
    RecommendationResponse,
    ChartsResponse,
)
from app.agent import run_agent
from app import tools
from app import groq_service


router = APIRouter(
    prefix="/api",
    tags=["Customer Segmentation Agent"]
)


# ----------------------------------------
# Health Check
# ----------------------------------------

@router.get(
    "/health",
    tags=["Health"],
    status_code=status.HTTP_200_OK
)
def health():

    return {
        "status": "healthy",
        "message": "Customer Segmentation Agent API is running."
    }


# ----------------------------------------
# Upload CSV
# ----------------------------------------

@router.post(
    "/upload",
    response_model=UploadResponse,
    tags=["Data Upload"],
    status_code=status.HTTP_201_CREATED
)
async def upload_file(
    file: UploadFile = File(...)
):

    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only .csv files are supported."
        )

    contents = await file.read()

    try:
        stats = tools.process_uploaded_csv(contents)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Could not parse CSV: {e}"
        )

    return UploadResponse(
        filename=file.filename,
        rows=stats["rows"],
        columns=stats["columns"],
        message=(
            "File validated successfully. Note: clustering on uploaded data "
            "isn't wired up yet -- this only confirms the file is readable."
        )
    )


# ----------------------------------------
# Chat Endpoint
# ----------------------------------------

@router.post(
    "/chat",
    response_model=ChatResponse,
    tags=["AI Agent"]
)
async def chat(
    request: ChatRequest
):

    chat_result = groq_service.generate_chat_response(request.query)

    return ChatResponse(**chat_result)


# ----------------------------------------
# Customer Segments
# ----------------------------------------

@router.get(
    "/segments",
    response_model=SegmentResponse,
    tags=["Segmentation"]
)
def get_segments():

    return SegmentResponse(
        segments=tools.segmentation_tool()
    )


# ----------------------------------------
# Customer Personas
# ----------------------------------------

@router.get(
    "/personas",
    response_model=PersonaResponse,
    tags=["Customer Personas"]
)
def get_personas():

    return PersonaResponse(
        personas=tools.personas_tool()
    )


# ----------------------------------------
# Product Recommendations
# ----------------------------------------

@router.get(
    "/recommendations",
    response_model=RecommendationResponse,
    tags=["Recommendations"]
)
def get_recommendations():

    return RecommendationResponse(
        recommendations=tools.recommendations_tool()
    )


# ----------------------------------------
# Charts
# ----------------------------------------

@router.get(
    "/charts",
    response_model=ChartsResponse,
    tags=["Visualization"]
)
def get_charts():

    return ChartsResponse(
        charts=tools.charts_tool()
    )