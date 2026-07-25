from pydantic import BaseModel


class CustomerInput(BaseModel):

    age: int

    job: str

    marital: str

    education: str

    housing: str

    loan: str

    annual_income: float

    credit_score: float

    account_balance: float

    digital_banking_score: float

    monthly_transactions: float

    investment_amount: float

    account_tenure: float

    number_of_products: int