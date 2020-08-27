# Web scraping challenge
UNC Data Analytics Bootcamp, August 2020

This repository scrapes several websites, realted to information about Mars, and then combines all of that into a new broswer app.

## Files included:
* Missions_to_Mars/mission_to_mars.ipynb
  * This is a Jupyter Notebook that scrapes the different sites and displays all of the collected information that we'll use in the web app.
* Missions_to_Mars/app.py
  * This is the main Flask app that calls scrape_mars.py and stores that scraped information into MongoDB, which is then called by the index.html and displayed.
* Missions_to_Mars/scrape_mars.py
  * This is the heart of the app. It does all of the scraping found in the Jupyter Notebook, but stores all of the resulting data in a single dictionary, which is then returned to app.py.
* templates/index.html
  * This is the underlying, base HTML for the web app.
* static/css/style.css
  * It's a CSS file to style index.html


## Pages scraped
* https://mars.nasa.gov/news/
  * This is where our Mars news title and description come from
* https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars
  * This is where the featured image comes from
* https://space-facts.com/mars/
  * This is where the table of Mars facts comes from
* https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars
  * This is where the 4 high quality Mars hemisphere images come from