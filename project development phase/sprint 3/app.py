from flask import Flask, render_template
import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
import numpy as np

app = Flask(__name__)

@app.route("/") #home route
def home():
    # dataset = [
    #     ('1',1),
    #     ('2',2),
    #     ('3',3),
    #     ('4',4),
    #     ('5',5)
    # ]
    # labels = [row[0] for row in dataset]
    # values = [row[1] for row in dataset]
    labels, values = getCrudeOilData(100)
    curr = 120 # temp
    return render_template("main_page.html", labels=labels, values=values, current_price=curr)

def getCrudeOilData(n = 100):
    file = "dataset\\Crude Oil Prices Daily.xlsx"
    df = pd.read_excel(file)
    labels = list(df["Date"].astype(str))
    df["Closing Value"].fillna(df['Closing Value'].mean(), inplace=True)
    values = list(df["Closing Value"])
    return labels[len(labels)-n:], values[len(values)-n:] # returning only the last n data


if __name__ == '__main__':
    app.run(debug=True)