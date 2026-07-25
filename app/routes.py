from fastapi import APIRouter, UploadFile, File, status

from app.schemas import (
    ChatRequest,
    ChatResponse,
    UploadResponse,
    SegmentResponse,
    PersonaResponse,
    RecommendationResponse,
    ChartsResponse,
)


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

    return UploadResponse(
        filename=file.filename,
        rows=0,
        columns=0,
        message="File uploaded successfully."
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

    return ChatResponse(
        response="This is a mock AI response.",
        execution_plan=[
            "Understand user query",
            "Identify required tools",
            "Generate response"
        ],
        results={}
    )


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
        segments=[
            {
                "id": 1,
                "name": "Young Professionals",
                "count": 250
            },
            {
                "id": 2,
                "name": "High Value Customers",
                "count": 120
            },
            {
                "id": 3,
                "name": "Senior Citizens",
                "count": 80
            }
        ]
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
        personas=[
            {
                "segment": "Young Professionals",
                "description":
                "Early career customers with moderate income and high digital engagement."
            },
            {
                "segment": "High Value Customers",
                "description":
                "Customers with high balances and premium banking needs."
            }
        ]
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
        recommendations=[
            {
                "segment": "Young Professionals",
                "products": [
                    "Travel Credit Card",
                    "Personal Loan"
                ]
            },
            {
                "segment": "High Value Customers",
                "products": [
                    "Wealth Management",
                    "Premium Savings Account"
                ]
            }
        ]
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
        charts={
            "pie": {},
            "bar": {},
            "scatter": {},
            "heatmap": {}
        }
    )