# running the backend locally
uvicorn fraud_api:app --reload

# running the frontend locally
cd frontend
npm run dev

# DataSet
data/card_transdata.csv was removed from the git repo due to file size.
card_transdata.csv can be downloaded from https://www.kaggle.com/datasets/dhanushnarayananr/credit-card-fraud
Then added to the data folder to retrain the model.

# AWS
Procfile tells AWS Elastic Beanstalk how to run the FastAPI backend startup.
requirements.txt tells AWS what dependencies to install.