"""
Churn Prediction API

Run with:
    litestar --app main:app run --reload
Then open:
    http://localhost:8000/schema/swagger
"""

from litestar import Litestar, get, post
from pydantic import BaseModel

from app.logger_setup import setup_logging
from app.model_utils import predict_churn

logger = setup_logging()


class ChurnRequest(BaseModel):
    CreditScore: float
    Age: float
    Tenure: float
    Balance: float
    NumOfProducts: float
    HasCrCard: float
    IsActiveMember: float
    EstimatedSalary: float
    Geography_Germany: int
    Geography_Spain: int
    Gender_Male: int


@get("/")
async def index() -> str:
    logger.info("home endpoint was accessed")
    return "Hello, world!, mohamed Fathi"


@get("/health")
async def health() -> dict[str, str]:
    logger.info("i sent a health ")
    return {"status": "healthy"}


@post("/predict", status_code=201)
async def predict(data: ChurnRequest) -> dict[str, float]:
    features = [
        data.CreditScore,
        data.Age,
        data.Tenure,
        data.Balance,
        data.NumOfProducts,
        data.HasCrCard,
        data.IsActiveMember,
        data.EstimatedSalary,
        data.Geography_Germany,
        data.Geography_Spain,
        data.Gender_Male,
    ]
    prediction = predict_churn(features)
    logger.info("f{features} was predicted as {prediction}")
    return {"prediction": prediction}


app = Litestar(
    route_handlers=[index, health, predict],
)
