import pymongo
from flask import Flask, render_template, jsonify
from scraping import get_groceries_data
from data_processing import calculate_values
import os
from dotenv import load_dotenv

load_dotenv(verbose=True)
DB_URI = os.getenv('DB_URI')

client = pymongo.MongoClient(DB_URI)
db = client.test003     # database name

app = Flask(__name__)

@app.route("/")
def index():
    # recieve data from mongoDB
    groceries_data = list(db.recipt.find())
    
    # sort by counts
    groceries_data_by_count = sorted(groceries_data, key=lambda elem: elem['count'], reverse=True)

    return render_template("index.html", data=groceries_data_by_count)


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