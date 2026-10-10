# running the backend locally
uvicorn fraud_api:app --reload

# running the frontend locally
cd frontend
npm run dev

# DataSet
data/card_transdata.csv was removed from the git repo due to file size.
card_transdata.csv can be downloaded from https://www.kaggle.com/datasets/dhanushnarayananr/credit-card-fraud
Then added to the data folder to retrain the model.