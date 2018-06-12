import datetime
import os
from flask import Flask, render_template, request, redirect
import requests as req
import json
import pandas as pd
import bokeh
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

print(os.getenv('PASSWORD'))
print(os.getenv('CUSTOM_USER'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/prices', methods=['POST'])
def prices():
    ticker = request.form.get('ticker')
    features = request.form.getlist('features')
    # call API
    # Or use requests module ot get json:
    quandl_api_key = os.getenv('QUANDL_API_KEY')
    date_start = '2017-01-01' # TODO custom dates
    date_end = '2017-12-31'

    if ticker == '':
        ticker = 'GOOG' # front end should give this

    url_params = {
        'ticker': ticker,
        'date.gte': date_start,  # month_ago.strftime('%Y-%m-%d'),#'1999-11-19,1999-11-22',
        'date.lte': date_end,
        'api_key': quandl_api_key
    }

    r = req.get('https://www.quandl.com/api/v3/datatables/WIKI/PRICES', params=url_params)

    if r.status_code != 200:
        print('API Error (' + str(r.status_code) + '): ' + r.reason) # throw error

    price_data = r.json()['datatable']

    colnames = [c['name'] for c in price_data['columns']]
    df = pd.DataFrame(data=price_data['data'], columns=colnames)
    data_obj = {col:df[col].tolist() for col in features}

    context = {'ticker': ticker, 'date': pd.to_datetime(df["date"]), 'data': json.dumps(data_obj)}

    return render_template('prices.html', d=context)

if __name__ == '__main__':
  app.run(port=33507)


# r.status_code
# r.headers['content-type']
# r.encoding
# r.text
# r.json()


# Postgres:
# from flask.ext.sqlalchemy import SQLAlchemy
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/${whoami}'
# db = SQLAlchemy(app)
