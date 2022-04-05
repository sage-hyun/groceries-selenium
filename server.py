import pymongo
from flask import Flask, render_template, jsonify
from scraping import get_groceries_data
from data_processing import calculate_values
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv(verbose=True)
DB_URI = os.getenv('DB_URI')

client = pymongo.MongoClient(DB_URI)
db = client.test003     # database name

app = Flask(__name__)

@app.route("/")
def index():
    # recieve data from mongoDB
    groceries_data = list(db.recipt.find())

    # flatten the 'date_list's to find the last order date
    flat_list = [date for elem in groceries_data for date in elem["date_list"]]
    last_order_date =  sorted(flat_list)[-1]

    # items bought once are unimportant
    groceries_data = [x for x in groceries_data if not x['count']==1 ]

    # calculate prediction
    for elem in groceries_data:        
        predicted_day = datetime.strptime(elem['predicted_day'], '%Y.%m.%d')
        diff = datetime.now() - predicted_day
        elem['prediction'] = (1 / (abs(diff.days) + 1)) * 100

    # sort by counts
    groceries_data_by_count = sorted(groceries_data, key=lambda elem: elem['count'], reverse=True)
    # sort by prediction
    groceries_data_by_prediction = sorted(groceries_data, key=lambda elem: elem['prediction'], reverse=True)

    return render_template("index.html", data={
        "by_count": groceries_data_by_count[:30],
        "by_prediction": groceries_data_by_prediction[:30],
    },
        last_order_date=last_order_date,
    )


@app.route("/scrape")
def scrape():
    get_groceries_data(db)   # scraping

    return jsonify({"code": 0, "msg": "Storage completed"})


@app.route("/process-data")
def process_data():
    calculate_values(db)

    return jsonify({"code": 0, "msg": "Calculation completed"})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8001)