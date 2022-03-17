from flask import Flask, render_template
from scraping import get_groceries_data

app = Flask(__name__)

@app.route("/")
def index():
    groceries_data = get_groceries_data()
    return render_template("index.html", data=groceries_data)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8001)