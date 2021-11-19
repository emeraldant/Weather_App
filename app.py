from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import requests
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
db = SQLAlchemy(app)
class City(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable=False)
@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        queryCity = request.form.get('city')
        if queryCity: #checking if city exists
            queryCityObj = City(name = queryCity)
            db.session.add (queryCityObj)
            db.session.commit()
    cities = City.query.all()
    urlCurrent = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=d97f97692b2c1b089aeb09c420503ae0&units=imperial'
    urlTrend = 'http://api.openweathermap.org/data/2.5/forecast?q={}&appid=d97f97692b2c1b089aeb09c420503ae0&units=imperial'
    weather_data = []
    for city in cities:
        curr = requests.get(urlCurrent.format(city.name)).json()
        trend = requests.get(urlTrend.format(city.name)).json()
        weather = {
            'city': city.name,
            'temperature' : curr['main']['temp'],
            'description' : curr['weather'][0]['description'],
            'day1': trend['list'][0]['main']['temp'],
            'day2': trend['list'][1]['main']['temp'],
            'day3': trend['list'][2]['main']['temp'],
            'day4': trend['list'][3]['main']['temp'],
            'day5': trend['list'][4]['main']['temp'],
            'icon': curr['weather'][0]['icon'],
        }
        weather_data.append(weather)
    return render_template('weather.html', weather=weather)
if __name__ == '__main__':
    app.run()
