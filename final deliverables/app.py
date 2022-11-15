from flask import Flask, render_template, url_for, flash, request, redirect
import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
import numpy as np

app = Flask(__name__)
app.config['SECRET KEY'] = "a5d6n3j4k5l6k7mn342nw3"

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
    curr = getCurrentCrudeOilPrice()
    return render_template("main_page.html", labels=labels, values=values, current_price=curr)

@app.route("/predict", methods=["GET","POST"])
def predictPage():
    if request.method == "POST":
        day1 = request.form['day-1']
        day2 = request.form['day-2']
        day3 = request.form['day-3']
        if not day1 or not day2 or not day3:
            flash('Enter all the past 3 days value')
        else:
            day1, day2, day3 = float(day1), float(day2), float(day3)
            price = getCurrentCrudeOilPrice([day1, day2, day3])
            return render_template('prediction.html', price=price)
    return render_template('prediction.html')
    pass

def getCrudeOilData(n = 100):
    file = "dataset\\Crude Oil Prices Daily.xlsx"
    df = pd.read_excel(file)
    labels = list(df["Date"].astype(str))
    df["Closing Value"].fillna(df['Closing Value'].mean(), inplace=True)
    values = list(df["Closing Value"])
    return labels[len(labels)-n:], values[len(values)-n:] # returning only the last n data

def getCurrentCrudeOilPrice(prices = []):
    model_file = "crude_oil_model.h5"
    file = "dataset\\Crude Oil Prices Daily.xlsx"

    df = pd.read_excel(file, usecols=[1])
    df["Closing Value"].fillna(df["Closing Value"].mean(), inplace=True)
    x = df.values

    # normalising 
    scaler = MinMaxScaler(feature_range=(0,1))
    x = scaler.fit_transform(x)

    if len(prices) == 0:
        data = np.reshape(x[len(x)-3:],(-1,1,3))
    else:
        prices = np.array(prices)
        data = np.reshape(prices, (-1,1,3))
    
    model = tf.keras.models.load_model(model_file)
    curr = model.predict(data)
    curr = scaler.inverse_transform(curr)
    return curr[0][0]


if __name__ == '__main__':
    app.run(debug=True)