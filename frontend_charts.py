import pandas as pd
import matplotlib.pyplot as mplot

#Create a dataframe for all charts to read from
df = pd.read_csv("data/card_transdata.csv")

# # # DISTANCE FROM HOME # # #
def createDistanceChartFromHome():
    groups = [0, 5, 10, 25, 50, 75, 100, 125, 150, 175, 200, 225, 250, 500, float("inf")]
    groupLabels = ["0-5", "5-10", "10-25", "25-50", "50-75", "75-100", "100-125", "125-150", "150-175", "175-200", "200-225", "225-250","250-500", "500+"]
    #add distance from home groups to the dataframe
    df["home_groups"] = pd.cut(df["distance_from_home"], bins=groups, labels=groupLabels)
    #add fraud as a percentage in the group field, observed false to keep rows with a 0 count in the results
    homeFraud = df.groupby("home_groups", observed=False)["fraud"].mean() * 100
    print(homeFraud)
    homeCount = df.groupby("home_groups",observed=False)["fraud"].count()
    print(homeCount)
    #start making the chart
    homeFraud.plot(kind="bar")
    mplot.title("Fraud Rate by Distance From Home")
    mplot.xlabel("Distance From Home")
    mplot.ylabel("Fraud Rate %")
    #condenses the chart to fit more data
    mplot.tight_layout()
    #save the chart to the front end files
    mplot.savefig("frontend/public/charts/fraud_by_home_distance.png")
    #close and move onto next chart
    mplot.close()



# # # DISTANCE FROM LAST TRANSACTION # # #
def createDistanceFromLast():
    lastTGroups = [0, 1, 5, 10, 25, 50, 100, 200, float("inf")]
    lastTGroupLabels = ["0-1", "1-5", "5-10", "10-25", "25-50", "50-100", "100-200", "200+"]
    #add distance from last transaction groups to the dataframe
    df["last_transaction_groups"] = pd.cut(df["distance_from_last_transaction"], bins=lastTGroups, labels=lastTGroupLabels)
    #add fraud as a percentage in the group field, observed false to keep rows with a 0 count in the results
    lastTFraud = df.groupby("last_transaction_groups", observed=False)["fraud"].mean() * 100
    print(lastTFraud)
    Count = df.groupby("last_transaction_groups",observed=False)["fraud"].count()
    print(Count)
    #start making the chart
    lastTFraud.plot(kind="bar")
    mplot.title("Fraud Rate by Distance From Last Transaction")
    mplot.xlabel("Distance from Last Transaction")
    mplot.ylabel("Fraud Rate %")
    #condenses the chart to fit more data
    mplot.tight_layout()
    #save the chart to the front end files
    mplot.savefig("frontend/public/charts/fraud_by_last_transaction.png")
    #close and move onto next chart
    mplot.close()



# # # Ratio To Purchase Price # # #
def createRatio():
    ratioGroups = [0, .5, 1, 2, 3, 4, 5, 7.5, 10, float("inf")]
    ratioGroupLabels = ["0-.5",".5-1", "1-2", "2-3", "3-4", "4-5", "5-7.5", "7.5-10", "10+"]
    #add ratio to purchase price groups to the dataframe
    df["ratio_groups"] = pd.cut(df["ratio_to_median_purchase_price"], bins=ratioGroups, labels=ratioGroupLabels)
    #add fraud as a percentage in the group field, observed false to keep rows with a 0 count in the results
    ratioFraud = df.groupby("ratio_groups", observed=False)["fraud"].mean() * 100
    print(ratioFraud)
    Count = df.groupby("ratio_groups",observed=False)["fraud"].count()
    print(Count)
    #start making the chart
    # ratioFraud.plot(kind="bar")
    ratioFraud.plot(kind="line", marker="o")
    mplot.title("Fraud Rate by Ratio to Median Purchase Price")
    mplot.xlabel("Ratio to Median Purchase Price")
    mplot.ylabel("Fraud Rate %")
    #condenses the chart to fit more data
    mplot.tight_layout()
    #save the chart to the front end files
    mplot.savefig("frontend/public/charts/fraud_by_purchase_ratio.png")
    #close and move onto next chart
    mplot.close()



# # # Boolean Charts # # #
def createBool():
    boolCols = ["repeat_retailer", "used_chip", "used_pin_number", "online_order"]
    boolLabels = ["Repeat Retailer", "Used Chip", "Used PIN", "Online Order"]
    #create a dictionary for each column
    fraudCounts = {}
    #loop through each and build values
    for col in boolCols:
        rates = df.groupby(col)["fraud"].sum()
        fraudCounts[col] = {
            "True": rates.get(1,0),
            "False": rates.get(0,0),
        }
    #test
    print(fraudCounts)
    #start making the chart
    boolDF = pd.DataFrame(fraudCounts).T
    boolDF.index = boolLabels
    boolDF.plot(kind="bar")
    mplot.title("Fraud Count by Transaction Characteristics")
    mplot.ylabel("Number of Fraudulent Transactions")
    mplot.xticks(rotation=45)
    mplot.tight_layout()
    #save the chart to the front end files
    mplot.savefig(
        "frontend/public/charts/fraud_by_boolean_features.png"
    )
    #close and move onto next chart
    mplot.close()



#Create Charts
createDistanceChartFromHome()
createDistanceFromLast()
createRatio()
createBool()