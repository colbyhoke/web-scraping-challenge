#------------------------------
# Colby Alexander Hoke
# UNC Data Analytics Bootcamp
# August 2020
#------------------------------

# Use MongoDB with Flask templating to create a new HTML page that displays all of the information that was scraped from the URLs above.
#
# Start by converting your Jupyter notebook into a Python script called scrape_mars.py 
#   with a function called scrape that will execute all of your scraping code from above
#   and return one Python dictionary containing all of the scraped data.
#
# Next, create a route called /scrape that will import your scrape_mars.py script and call your scrape function.
# Store the return value in Mongo as a Python dictionary.
# Create a root route / that will query your Mongo database and pass the mars data into an HTML template to display the data.
# Create a template HTML file called index.html that will take the mars data dictionary and
#   display all of the data in the appropriate HTML elements. Use the following as a guide for what the final product should look like, but feel free to create your own design.


from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time

def init_browser():
    
    # Mac path
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}

    #Windows path
    #executable_path = {"executable_path": "chromedriver.exe"}

    return Browser("chrome", **executable_path, headless=False)

def scraper():
    
    ###############################################################
    # NASA Mars News Site:
    # https://mars.nasa.gov/news

    # Collect the latest News Title and Paragraph Text.
    # Assign the text to variables.
    #
    # Output:
    #   news_title
    #   news_p
    ###############################################################
    
    browser = init_browser()

    nasa_news_url = 'https://mars.nasa.gov/news/'
    browser.visit(nasa_news_url)

    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    article = soup.find('div', class_='list_text')
    
    news_title = article.find('a').text
    news_p = article.find('div', class_='article_teaser_body').text

    ###############################################################
    # JPL Featured Space Image
    # https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars
    #
    # Find the full size image url for the current Featured Mars Image
    #
    # Output:
    #   featured_image_url
    ###############################################################

    space_img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    url_split = space_img_url.split('/spaceimages',1)

    browser.visit(space_img_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    img_link = soup.find('section', class_='main_feature').find('a', class_='button fancybox')['data-link']
    img_page_url = url_split[0] + img_link

    # Visit that page and parse the HTML
    browser.visit(img_page_url)
    
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Pull the full res image URL
    img_details = soup.find('div', id='secondary_column').find_all('div', class_='download_tiff')
    hires_image_url = img_details[1].find('a')['href']

    # Append to the URL
    featured_image_url = 'https:' + hires_image_url

    ###############################################################
    # Mars facts
    # https://space-facts.com/mars/
    # 
    # Use pandas to read tables
    # Convert the relevant dataframe to an html table
    #
    # Output:
    #   mars_html_table
    ###############################################################

    # Set URL to pull from
    mars_facts_url = 'https://space-facts.com/mars/'

    # Read and store all of the tables
    tables = pd.read_html(mars_facts_url)

    # Get the table we want
    mars_df = tables[0]

    # Give columns names and reset the index
    mars_df.columns=['Description','Mars']
    mars_df.set_index('Description', inplace=True)

    # Convert the table to HTML and strip the new line returns
    mars_html_table = mars_df.to_html()
    mars_html_table = mars_html_table.replace('\n', '')

    ###############################################################
    # Mars hemispheres images
    # 
    ###############################################################
    usgs_astro_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    # Split the URL to use later
    usgs_astro_url_split = usgs_astro_url.split('/search',1)

    # Visit the page
    browser.visit(usgs_astro_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    usgs_astro_products = soup.find('div', class_='collapsible results')

    hemisphere_pages = usgs_astro_products.find_all('div', class_='item')

    # List where everything will be stored
    hemisphere_image_urls = []

    for page in hemisphere_pages:
        # Clear the dictionary for each iteration
        hemisphere_dict = {}
        
        # Find the title and add it to the dictionary
        title = page.find('div', class_='description').find('a').text
        hemisphere_dict['title'] = title
        
        # Find the link to the detail page
        hemisphere_link = page.find('div', class_='description').find('a')['href']
        
        # Visit the page and parse it
        browser.visit(usgs_astro_url_split[0] + hemisphere_link)
        hemisphere_html = browser.html
        hemisphere_soup = BeautifulSoup(hemisphere_html, 'html.parser')
        
        # Find the link to the full image and add it to the dictionary
        img_link = hemisphere_soup.find('div', class_='content').find('a')['href']
        hemisphere_dict['img_url'] = img_link
        
        # Add the filled dictionary to the list
        hemisphere_image_urls.append(hemisphere_dict)
        
        # Go a page back, ready for the next iteration
        browser.back()
        
    hemisphere_image_urls
    ###############################################################
    # Close the browser after scraping
    ###############################################################
    browser.quit()

    ###############################################################
    # Put it all in a dictionary
    ###############################################################

    mars_data = {
        "news_title" : news_title,
        "news_p" : news_p,
        "featured_image_url" : featured_image_url,
        "mars_html_table" : mars_html_table,
        'hemisphere_image_urls' : hemisphere_image_urls
    }

    ###############################################################
    # Return results
    ############################################################### 
    return mars_data