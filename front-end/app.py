# import flask
from flask import Flask, render_template, request, redirect, session
import json
from flask_cors import CORS
import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
import pandas as pd
from sklearn.neural_network import MLPRegressor

app = Flask(__name__)
CORS(app)
@app.post("/")
def getData():
    a = request.get_json()
    modelL = pickle.load(open('model', 'rb'))
    scaler = pickle.load(open('scaler', 'rb'))
    data = [int(a["ws"]),int(a["twopa"]),int(a["fga"]),int(a["twop"]),int(a["pts"]),int(a["fg"])]
    data = [data]
    predictionL = modelL.predict(scaler.transform(data))

    return str(predictionL[0])