from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from predict import predict_fraud_transaction

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173",
                   "https://main.d3sev77tjydmfh.amplifyapp.com",
                   "https://d3qnz1pzf2tly3.cloudfront.net"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Transaction(BaseModel):
    distance_from_home: float
    distance_from_last_transaction: float
    ratio_to_median_purchase_price: float
    repeat_retailer: bool
    used_chip: bool
    used_pin_number: bool
    online_order: bool

@app.post("/predict")
def predict(transaction: Transaction):
    return predict_fraud_transaction(transaction.model_dump())