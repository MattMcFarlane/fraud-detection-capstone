import joblib
import pandas as pd

#load the fraud model
model = joblib.load("models/fraud_model.joblib")
#save the validation threshold from testing
threshold = .6

def predict_fraud_transaction(transaction_data):
    #convert booleans to 1 or 0
    transaction_data["repeat_retailer"] = int(transaction_data["repeat_retailer"])
    transaction_data["used_chip"] = int(transaction_data["used_chip"])
    transaction_data["used_pin_number"] = int(transaction_data["used_pin_number"])
    transaction_data["online_order"] = int(transaction_data["online_order"])

    #generate the transaction from passed data
    transaction = pd.DataFrame([transaction_data])

    # get probability of fraud
    fraud_probability = model.predict_proba(transaction)[:, 1][0]

    # check if the fraud probability exceeds threshold
    fraud = fraud_probability >= threshold

    return {
        "fraud_probability": fraud_probability,
        "flagged_as_fraud": bool(fraud)
    }


#create a test transaction
test_data = {
    "distance_from_home": 10.0,
    "distance_from_last_transaction": 200,
    "ratio_to_median_purchase_price":10.2,
    "repeat_retailer": True,
    "used_chip": False,
    "used_pin_number": True,
    "online_order": False
}
#get test
test_results = predict_fraud_transaction(test_data)

print("Fraud Probability Raw:", test_results["fraud_probability"])
print(f"Fraud Probability: {test_results["fraud_probability"]:.2%}")
print("Flagged As Fraud:", test_results["flagged_as_fraud"])