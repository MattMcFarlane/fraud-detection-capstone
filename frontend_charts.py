import pandas as pd
import matplotlib.pyplot as mplot
from matplotlib import pyplot as plt

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
            "True": rates.get(1),
            "False": rates.get(0),
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
    mplot.savefig("frontend/public/charts/fraud_by_boolean_features.png")
    #close and move onto next chart
    mplot.close()

# # # Boolean Charts # # #
def createFraudCountPie():
    #count fraud and non fraud
    fraudFullCount = df["fraud"].value_counts()
    # print(fraudCount)

    #get counts
    fraudCounts = [fraudFullCount.get(0), fraudFullCount.get(1)]

    labels = ["Not Fraud", "Fraud"]

    #create the pie chart, autopct adds labels XX.X%
    mplot.pie(fraudCounts, labels=labels, autopct="%1.1f%%")
    mplot.title("Fraud Distribution")

    #save the chart to the front end files
    mplot.savefig("frontend/public/charts/fraud_distribution.png")

    #close and move onto next chart
    mplot.close()

# # # Correlation Matrix # # #
def createCorrelationMatrix():
    columns = ["distance_from_home",
        "distance_from_last_transaction",
        "ratio_to_median_purchase_price",
        "repeat_retailer",
        "used_chip",
        "used_pin_number",
        "online_order",
        "fraud"]
    labels = [
        "Home Distance",
        "Last Transaction",
        "Purchase Ratio",
        "Repeat Retailer",
        "Used Chip",
        "Used PIN",
        "Online Order",
        "Fraud"
    ]

    #calculate correlations
    correlations = df[columns].corr()

    #hide diagnoal correlations
    for i in range(len(columns)):
        correlations.iloc[i, i] = float("nan")

    #create heatmap
    figure, axis = mplot.subplots(figsize=(10, 8))
    #copy the color map and set nan (bad values) to grey. Sets center boxes as grey
    greymap = mplot.cm.viridis.copy()
    greymap.set_bad(color="gray")

    heatmap = axis.imshow(correlations, cmap=greymap, vmin=-0.5, vmax=0.5)

    # add axis labels
    #rotate labels 45 deg to avoid them from overlapping with eachother, ha = horizontal align right to align with the tick mark
    axis.set_xticks(range(len(labels)), labels=labels, rotation=45, ha="right")
    axis.set_yticks(range(len(labels)), labels=labels)

    # show correlation value inside each square
    for row in range(len(labels)):
        for col in range(len(labels)):
            axis.text(
                col,
                row,
                f"{correlations.iloc[row, col]:.4f}",
                ha="center",
                va="center"
            )

    figure.colorbar(heatmap, label="Correlation")
    mplot.title("Feature Correlation Matrix")
    #tight layout to keep everything in the image
    mplot.tight_layout()

    #save chart
    mplot.savefig(
        "frontend/public/charts/correlation_heatmap.png"
    )

    mplot.close()

#Create Charts
createDistanceChartFromHome()
createDistanceFromLast()
createRatio()
createBool()
createFraudCountPie()
createCorrelationMatrix()