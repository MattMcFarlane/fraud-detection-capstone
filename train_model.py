# This is a sample Python script.
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix, f1_score


csvFile = "data/card_transdata.csv"
df = pd.read_csv(csvFile)

# print(df.head())
# print(df.shape)
# print(df.info())
# print(df.isnull().sum())
#
# print("\n\n\n# Check for duplicate rows")
# # Check for duplicate rows
# print("Duplicates:", df.duplicated().sum())
#
# print("\n\n\n# View summary statistics")
# # View summary statistics
# # pd.set_option("display.max_columns", None)
# print(df.describe())
#
# print("\n\n\n# View summary statistics")
# # Check fraud distribution
# print(df["fraud"].value_counts())
#
# print("\n\n\n# Check fraud percentage")
# # Check fraud percentage
# print(df["fraud"].value_counts(normalize=True))


#start training
#drop and set output column and target
x = df.drop("fraud", axis=1)
y = df["fraud"]

#set up training and test sets
#split test_size to 80% training data, 20% testing data into a temp variable
#set random state to fixed number to reproduce static pseudo randomness
#add stratify to maintain original fraud rate between training and test data
x_train, x_temp, y_train, y_temp = train_test_split(x, y, test_size=0.2, random_state=7007, stratify=y)

# split the temporary data into validation and testing 10% each.
x_validation, x_test, y_validation, y_test = train_test_split(x_temp, y_temp, test_size=0.5, random_state=7007, stratify=y_temp)

# #test
# #print col / rows of data
# print(x_train.shape)
# print(x_test.shape)
# #print number of fraud values
# print(y_train.value_counts())
# print(y_test.value_counts())

#scale non-boolean columns to optimize training
#define which columns will be scaled
to_scale_columns = [
    "distance_from_home",
    "distance_from_last_transaction",
    "ratio_to_median_purchase_price"
]
#scale columns
preprocessor = ColumnTransformer(
    transformers=[
        ("scale", StandardScaler(), to_scale_columns)
    ],
    remainder="passthrough"
)
#build the model pipline
model = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", LogisticRegression())
])
#train the model
model.fit(x_train, y_train)

# Tests
# # make predictions using test data
# y_pred = model.predict(x_test)
#
# print("Accuracy:", accuracy_score(y_test, y_pred))
# print("Precision:", precision_score(y_test, y_pred))
# print("Recall:", recall_score(y_test, y_pred))
#
# print("\nConfusion Matrix:")
# print(confusion_matrix(y_test, y_pred))


# Tests for different thresholds
#get probabilities for every row, col 1
validation_probabilities = model.predict_proba(x_validation)[:,1]

#build thresholds to test
validation_thresholds = [.05, .1, .15, .2, .25, .3, .35, .4, .45, .5, .55, .6, .65, .7, .75, .8, .85, .9, .95]
#save validation results
validation_results = []
#test each
print("TESTING THRESHOLDS")
for threshold in validation_thresholds:
    validation_prediction = (validation_probabilities >= threshold).astype(int)

    #get the confusion matrix values
    tn, fp, fn, tp = confusion_matrix(y_validation, validation_prediction).ravel()

    #save results
    validation_results.append({
        "threshold": threshold,
        "accuracy": accuracy_score(y_validation, validation_prediction),
        "precision": precision_score(y_validation, validation_prediction),
        "recall": recall_score(y_validation, validation_prediction),
        "f1": f1_score(y_validation, validation_prediction),
        "true_negative": tn,
        "false_positive": fp,
        "false_negative": fn,
        "true_positive": tp
    })

    #also print results to consol
    print()
    print("Threshold: " + str(threshold))
    print("Accuracy: ", accuracy_score(y_validation, validation_prediction))
    print("Precision: ", precision_score(y_validation, validation_prediction))
    print("Recall: ", recall_score(y_validation, validation_prediction))
    print("F1 Score: ", f1_score(y_validation, validation_prediction))
    print("Confusion Matrix: ")
    print(confusion_matrix(y_validation, validation_prediction))

#convert results to dataframe and save csv, use no index false to prevent an index column
pd.DataFrame(validation_results).to_csv("data/validation_results.csv", index=False)

#use .3 as the chosen threshold and test again
final_threshold = 0.60

test_probabilities = model.predict_proba(x_test)[:, 1]
test_prediction = (test_probabilities >= final_threshold).astype(int)

#save final result
tn, fp, fn, tp = confusion_matrix(y_test, test_prediction).ravel()

final_results = [{
    "threshold": final_threshold,
    "accuracy": accuracy_score(y_test, test_prediction),
    "precision": precision_score(y_test, test_prediction),
    "recall": recall_score(y_test, test_prediction),
    "f1": f1_score(y_test, test_prediction),
    "true_negative": tn,
    "false_positive": fp,
    "false_negative": fn,
    "true_positive": tp
}]

pd.DataFrame(final_results).to_csv("data/final_test_results.csv", index=False)

print()
print("FINAL TEST RESULTS")
print("Threshold:", final_threshold)
print("Accuracy:", accuracy_score(y_test, test_prediction))
print("Precision:", precision_score(y_test, test_prediction))
print("Recall:", recall_score(y_test, test_prediction))
print("F1 Score:", f1_score(y_test, test_prediction))
print("Confusion Matrix:")
print(confusion_matrix(y_test, test_prediction))

#
# #save the model for future use.
joblib.dump(model, "models/fraud_model.joblib")