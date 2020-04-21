from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import mars_scrape2
import os




app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def home():

      mars_info = mongo.db.mars_info.find_one()
    
      return render_template("index1.html",mars_info = mars_info)

@app.route("/scrape")
def scrape():

      mars_info = mongo.db.mars_info
      mars_data = mars_scrape2.mars_news.new_title()
      mars_data = mars_scrape2.mars_news.new_p()
      mars_data = mars_scrape2.featured_image.img_url()
      mars_data = mars_scrape2.twitter_weather.mars_weather()
      mars_data = mars_scrape2.mars_facts.df.to_html()
      mars_data = mars_scrape2.Hemispheres.hemisphere_image_urls()
      mars_info.update({}, mars_data, upsert=True)
      return redirect("/", code=302)

if __name__== "__main__":
    app.run(debug=True)    
