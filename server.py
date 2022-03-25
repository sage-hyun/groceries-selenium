import pymongo
from flask import Flask, render_template, jsonify
from scraping import get_groceries_data
import os
from dotenv import load_dotenv

load_dotenv(verbose=True)
DB_URI = os.getenv('DB_URI')

client = pymongo.MongoClient(DB_URI)
db = client.test001     # database name

app = Flask(__name__)

@app.route("/")
def index():
    # recieve data from mongoDB
    groceries_data = list(db.recipt.find())

    return render_template("index.html", data=groceries_data)


@app.route("/scrape")
def scrape():
    groceries_data = get_groceries_data()   # scraping

    # add data to mongoDB
    db.recipt.insert_many(groceries_data)
    return jsonify({"code": 0, "msg": "Storage completed"})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8001)