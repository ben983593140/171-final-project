from flask import Flask, render_template, request
import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
import pandas as pd

ATTRIBUTES = ['WS', '2PA', 'FGA', '2P', 'PTS', 'FG']

app = Flask(__name__)

@app.route('/form')
def form():
    return render_template('form.html')
 
@app.route('/', methods = ['POST', 'GET'])
def data():
    if request.method == 'GET':
        model = pickle.load(open('linear_model', 'rb'))

        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        form_data = request.form

        
        scaler = pickle.load(open('linear_scaler', 'rb'))
        data = form_data[ATTRIBUTES]
        data = pd.DataFrame(data)
        prediction = model.predict(scaler.transform(data))
        

        return render_template('data.html', salary = 1000)
 
 
if __name__ == '__main__':
    app.run(host='localhost', port=5000)