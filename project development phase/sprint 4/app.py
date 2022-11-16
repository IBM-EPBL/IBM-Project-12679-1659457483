from flask import Flask, render_template, url_for, flash, request, redirect
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import requests

app = Flask(__name__)
app.config['SECRET KEY'] = "a5d6n3j4k5l6k7mn342nw3"

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "AR9lZEewgN6dKPbjnLA46dB-sTUsO08rbIs_8BarVNXc"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

file = "dataset\\Crude Oil Prices Daily.xlsx"
df = pd.read_excel(file)
df["Closing Value"].fillna(df["Closing Value"].mean(), inplace=True)
x = df["Closing Value"].values.reshape(-1,1)

# normalising 
scaler = MinMaxScaler(feature_range=(0,1))
x = scaler.fit_transform(x)

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
    curr = getCrudeOilPriceCloud([values[-3],values[-2],values[-1]])
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
            # price = getCurrentCrudeOilPrice([day1, day2, day3])
            price = getCrudeOilPriceCloud([day1, day2, day3])
            return render_template('prediction.html', price=price)
    return render_template('prediction.html')
    pass

def getCrudeOilData(n = 100):
    labels = list(df["Date"].astype(str))
    df["Closing Value"].fillna(df['Closing Value'].mean(), inplace=True)
    values = list(df["Closing Value"])
    return labels[len(labels)-n:], values[len(values)-n:] # returning only the last n data

def getCrudeOilPriceCloud(prices=[]):
    data = [[prices]]

    payload_scoring = {"input_data": [{"fields": [["day-1","day-2","day-3"]], "values": data}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/8f848e93-fea8-40c6-a991-43c14c6329e5/predictions?version=2022-11-16', json=payload_scoring,
     headers={'Authorization': 'Bearer ' + mltoken})
    response = response_scoring.json()['predictions'][0]["values"]
    res = scaler.inverse_transform(response)
    return round(res[0][0],4)
    

if __name__ == '__main__':
    app.run(debug=True)