Crude Oil Price Prediction

dataset -> downloaded from kaggle : "Crude Oil Prices Daily.xlsx"

Dataset description:
contains two columns:-

1.  date
2.  Closing Prices

Model:
-> Combination of LSTM and GRU is used to make the final prediction

The model is created by using the script in the final deliverables/crude_oil_price_predictor.ipynb
The model is saved as "crude_oil_model.h5"

Front end:
Flask is used to provide the frontend for the system

The front end is a single page system which shows the current price based on the last 10 days closing prices obtained from the dataset

A graph which visualises the last 100 days closing days prices is also added

## to run:

run the app.py to run the flask app

## Link of the deployed website:

https://crude-oil-price-predictor.onrender.com/

## Link for the demo link video

https://drive.google.com/file/d/14IRnVnVVUTtkxxm8JilmtiKw-i4Wow6g/view?usp=sharing

## demo YouTube link

https://youtu.be/ippu7rPWVSI
