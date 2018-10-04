#import necessary libraries
from flask import Flask, render_template
import pymongo
import scrape_mars

app = Flask(__name__)

client = pymongo.MongoClient()
db = client.missiontomars_db
collection = db.mars_things

@app.route("/")
def home():
    data = list(db.collection.find())[0]
    return render_template('index.html', mars_things=data)

@app.route("/scrape")
def scrape():
    mars_things = db.collection
    mars_data = scrape_mars.scrape()
    mars_things.update(
        {},
        mars_data,
        upsert=True
    )
    return "Successful Scrape"

if __name__ == "__main__":
    app.run(debug=True)
