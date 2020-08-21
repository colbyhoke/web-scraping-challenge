#------------------------------
# Colby Alexander Hoke
# UNC Data Analytics Bootcamp
# August 2020
#------------------------------

from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Establish Mongo connection with PyMongo
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route("/")
def home():

    # Find one record of data from the mongo database
    mars_data = mongo.db.mars_info.find_one()

    # Return template and data
    return render_template("index.html", mars_data = mars_data)

@app.route("/scrape")
def scrape():
 # Run the scrape function
    mars_data_scrape = scrape_mars.scraper()

    # Update the Mongo database using update and upsert=True
    mongo.db.mars_info.update({}, mars_data_scrape, upsert=True)

    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)