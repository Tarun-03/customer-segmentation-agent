from fastapi import APIRouter
from .services import CustomerService
from fastapi import HTTPException
from .schemas import CustomerInput

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