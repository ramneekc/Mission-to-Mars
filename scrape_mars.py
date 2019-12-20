from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
from flask import Markup

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    headline = {}
#     to find the latest headlines
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    results = soup.find_all('li', class_="slide")
    headline['news_title'] = results[0].find('h3').text
    headline['news_p'] = results[0].find('div', class_="rollover_description_inner").text
    
#     to find the featured image
    url1 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url1)
    html = browser.html
    soup = bs(html, 'html.parser')
    results = soup.find('div', class_="carousel_items")
    article = results.find('article')
    img_url_2 = article.find('a',id="full_image")['data-fancybox-href']
    img_ulr_1 = 'https://www.jpl.nasa.gov/'
    headline['featured_image_url'] = img_ulr_1 + img_url_2
    
#     to find the latest weather
    url2 = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url2)
    html = browser.html
    soup = bs(html, 'html.parser')
    results = soup.find_all('li', class_="js-stream-item stream-item stream-item")
    for i in range(10):
        x = results[i].find('div',class_="js-tweet-text-container").text
        if "insight" in x.lower():
            headline['mars_weather'] = x
#     headline['mars_weather'] = results[0].find('div',class_="js-tweet-text-container").text
    
#     to find mars facts and put them in a table
    url3 = 'https://space-facts.com/mars/'
    tables = pd.read_html(url3)
    df = tables[0]
    html_table = df.to_html()
    headline['mars_facts'] = html_table.replace('\n', '')
    
#     to find the hemisphere images
    url4 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url4)
    html = browser.html
    soup = bs(html, 'html.parser')
    results = soup.find('div', class_="collapsible results")
    x = results.find_all('div',class_="description")

    base_url = "https://astrogeology.usgs.gov"
    hemisphere_image_list = []
    for result in x:
        hemisphere_image_dict = {}
        y = result.find('h3').text
        itemlink = result.find('a',class_="itemLink product-item")
        url_1 = itemlink['href']
        url_2 = base_url + url_1
        browser.visit(url_2)
        html_1 = browser.html
        soup_1 = bs(html_1, 'html.parser')
        results_1 = soup_1.find('img', class_="wide-image")
        url_3 = results_1['src']
        url_4 = base_url + url_3
    
        hemisphere_image_dict["title"]=y
        hemisphere_image_dict["img_url"]=url_4
        hemisphere_image_list.append(hemisphere_image_dict)
    headline['mars_hemispheres'] = hemisphere_image_list
    
    
    browser.quit()

    return headline
