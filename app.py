import os
from flask import Flask, render_template, request, redirect
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

if __name__ == '__main__':
  app.run(port=33507)


# from flask.ext.sqlalchemy import SQLAlchemy
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/[YOUR_DATABASE_NAME]'
# db = SQLAlchemy(app)