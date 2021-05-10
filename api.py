import requests
from datetime import date, timedelta, datetime

from flask import Flask, render_template
app = Flask(__name__)

BASE_URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=389&date="

def days_cur_month():
    m = datetime.now().month
    y = datetime.now().year
    ndays = (date(y, m+1, 1) - date(y, m, 1)).days
    d1 = date(y, m, 1)
    d2 = date(y, m, ndays)
    delta = d2 - d1

    return [(d1 + timedelta(days=i)).strftime('%d-%m-%Y') for i in range(delta.days + 1)]

def get_availability(adate):
    centerFound = False

    URL = BASE_URL+ adate
    print(URL)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    states = requests.get(URL, headers=headers)
    centers = states.json()['centers']
    for center in centers:
        for validSession in center['sessions']:
            if validSession['min_age_limit'] == 18:
                if validSession['available_capacity'] > 0:
                    centerFound = True

    return centerFound, centers

dates = days_cur_month()

availability = []

# for d in dates:
#     availability.append((d, get_availability(d)))

# print(availability)

@app.route('/api/v1/getAvailability/<date>')
def getAvailability(date=None):
    availability, centers = get_availability(date)
    return render_template('index.html', date=date, availability=availability, centers=centers)


@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run()