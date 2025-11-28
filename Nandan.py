# importing all the required python modules

from bs4 import BeautifulSoup
from utils.disease import disease_dic
from utils.model import ResNet9
from PIL import Image
from torchvision import transforms
import torch
import io
from datetime import datetime
import urllib.parse
from utils.fertilizer import fertilizer_dic
from utils.crop import crop

import plotly.express as px
import plotly
import json
from flask import Flask, flash, redirect, request, render_template, session, url_for
from markupsafe import Markup
import pickle
import pandas as pd
import requests

import numpy as np
from mongoengine import connect, Document, StringField, DateTimeField
from werkzeug.security import generate_password_hash, check_password_hash


# Flask app setup
app = Flask(__name__)
app.secret_key = 'aifarming'

# MongoDB connection
connect(
    db='aifarming_db',
    host='localhost',
    port=27017
)


# MongoDB Models
class Users(Document):
    username = StringField(required=True)
    email = StringField(required=True, unique=True)
    phone = StringField()
    profession = StringField()
    password = StringField(required=True)
    rpassword = StringField()
    registered_Date = DateTimeField(default=datetime.now)


class Market(Document):
    fname = StringField(required=True)
    lname = StringField(required=True)
    email = StringField(required=True)
    phone = StringField()
    address = StringField()
    croptype = StringField()
    quantity = StringField()
    cropname = StringField()
    msp = StringField()
    registered_Date = DateTimeField(default=datetime.now)


# Login Function
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        _email = request.form['email']
        _password = request.form['password']
        user = Users.objects(email=_email).first()

        if user and check_password_hash(user.password, _password):
            session['logged_in'] = user.username
            return redirect(url_for('home'))
        else:
            return render_template('login.html', errormsg="Invalid email/password")

    return render_template('login.html')


# Signup Function
@app.route('/signup', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        _username = request.form['uname']
        _email = request.form['email']
        _phone = request.form['phone']
        _profession = request.form.get('profession', '')
        _password = request.form['password']
        _rpassword = request.form['rpassword']

        if _password != _rpassword:
            return render_template("signup.html", msg="Passwords do not match")

        if Users.objects(email=_email).first():
            return render_template("signup.html", msg="User already exists")

        usersave = Users(
            username=_username,
            email=_email,
            phone=_phone,
            profession=_profession,
            password=generate_password_hash(_password),
            rpassword=generate_password_hash(_rpassword)
        )
        usersave.save()
        return redirect('/login')

    return render_template("signup.html")

# =======================
# Load ML models
# =======================

# Crop recommendation model
model = pickle.load(open('./pickle/crops.pkl', 'rb'))

# Fertilizer model (may fail due to sklearn version mismatch)
try:
    with open('./pickle/fertilizer1.pkl', 'rb') as f:
        fert = pickle.load(f)
except Exception as e:
    print("Warning: could not load fertilizer model:", e)
    fert = None  # so app won't crash


# Weather API
def weather_fetch(city_name):
    api_key = '3b0124dbadcdbcf295fd8c009f8efc0c'
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}appid={api_key}&q={city_name}"
    x = requests.get(complete_url).json()
    if x.get("cod") != "404":
        y = x["main"]
        return round((y["temp"] - 273.15), 2), y["humidity"]
    return None


@app.route('/')
def home():
    return render_template("index.html")


# Crop Prediction Route
@app.route('/crop', methods=['GET', 'POST'])
def predict():
    if request.method == "POST":
        N = int(request.form['Nitrogen'])
        K = int(request.form['Potassium'])
        P = int(request.form['Phosphorous'])
        city = request.form['city']
        rainfall = int(request.form['Rainfall'])
        ph = float(request.form['PH'])

        weather = weather_fetch(city)
        if weather is None:
            return render_template("crop.html", prediction_text="Weather API Error!")

        temperature, humidity = weather
        prediction = model.predict([[N, K, P, temperature, humidity, ph, rainfall]])[0]
        cropdata = crop[prediction]

        return render_template("crop.html",
                               prediction_text=prediction.capitalize(),
                               yield_value=cropdata["yield"],
                               growing_season=cropdata["growing_season"],
                               pests_and_diseases=", ".join(cropdata["pests_and_diseases"]),
                               varieties=", ".join(cropdata["varieties"]),
                               prices=", ".join([f"{k}: ₹{v}" for k, v in cropdata["price_per_kg"].items()])
                               )
    return render_template("crop.html")


# Disease Prediction
disease_classes = list(disease_dic.keys())
model_path = './pickle/plant_disease_model.pth'

disease_model = ResNet9(3, len(disease_classes))
disease_model.load_state_dict(torch.load(model_path, map_location='cpu'))
disease_model.eval()


def predict_image(img):
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.ToTensor(),
    ])
    image = Image.open(io.BytesIO(img)).convert('RGB')
    img_u = torch.unsqueeze(transform(image), 0)

    with torch.no_grad():
        _, preds = torch.max(disease_model(img_u), dim=1)

    return disease_classes[preds[0].item()]


@app.route('/disease', methods=['GET', 'POST'])
def disease():
    if request.method == 'POST':
        file = request.files['file']
        img = file.read()
        pred = predict_image(img)
        return render_template('disease.html', prediction=Markup(disease_dic[pred]))

    return render_template('disease.html')


@app.route('/news')
def news():
    url = 'https://agriculturepost.com/category/farm-inputs/'
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    news_data = []

    for item in soup.find_all('article'):
        news_data.append({
            'title': item.find('h3').text if item.find('h3') else '',
            'image': item.find('img')['src'] if item.find('img') else '',
            'link': item.find('a')['href'] if item.find('a') else ''
        })
    return render_template('news.html', dict=news_data)


@app.route('/weather')
def weather():
    return render_template('weather.html')


if __name__ == "__main__":
    app.run(debug=True)
