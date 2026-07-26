from fastapi import APIRouter
from .services import CustomerService
from .schemas import CustomerInput, ChatRequest, ChatResponse
from fastapi import HTTPException
from app import groq_service

router = APIRouter()

service = CustomerService()


@router.get("/")
def home():

    return {
        "message": "Customer Segmentation API Running"
    }


@router.get("/clusters")
def clusters():

    return service.get_clusters()


@router.get("/personas")
def personas():

    return service.get_personas()


@router.get("/recommendations")
def recommendations():

    return service.get_recommendations()

@router.get("/customers/{customer_id}")
def customer(customer_id: str):

    result = service.get_customer(customer_id)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return result

@router.post("/predict")
def predict(customer: CustomerInput):

    result = service.predict_customer(
        customer.model_dump()
    )

    return result

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    chat_result = groq_service.generate_chat_response(request.query)
    return ChatResponse(**chat_result)