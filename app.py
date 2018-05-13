from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import Mongo_Web_Scrape


app = Flask(__name__)


mongo = PyMongo(app)


@app.route('/')
def index():
    space = mongo.db.space.find_one()
    print(space)
    return render_template('index.html', space=space)


@app.route('/scrape')
def scrape():
    space = mongo.db.space
    data = Mongo_Web_Scrape.scrape()
    space.update(
        {},
        data,
        upsert=True
    )
    return redirect("http://localhost:5000/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
