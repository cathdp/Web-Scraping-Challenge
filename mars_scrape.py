from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import re
import time


def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

mars_info ={}

def scrape_mars_news():
    browser = Browser('chrome',executable_path='chromedriver',headless=False)
        
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    browser.is_element_present_by_css('ul.item_list li.slide')
    html = browser.html
    
    news_soup = bs(html, 'html.parser')
    
    slide_elem = news_soup.select_one('ul.item_list li.slide')
    slide_elem.find('div',class_='content_title')
    
    news_title = slide_elem.find('div',class_='content_title').get_text()
    
    news_p = slide_elem.find('div',class_='article_teaser_body').get_text()
    
    mars_info['news_title'] = news_title
    mars_info['news_paragraph'] = news_p

    browser.quit()

    return mars_info

def scrape_mars_image():
    try:
        browser = init_browser()
        
        url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(url)
        
        full_image_elem = browser.find_by_id('full_image')
        full_image_elem.click()
        
        browser.is_element_present_by_text('more info', wait_time=1)
        more_info_elem = browser.find_link_by_partial_text('more info')
        more_info_elem.click()
        
        
        html = browser.html
        img_soup = bs(html, 'html.parser')
    
        img_url_rel = img_soup.select_one('figure.lede a img').get('src')
        img_url_rel
        
        img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
        img_url
        
        featured_image_url = img_url_rel + img_url
        featured_image_url 
        
        mars_info['featured_image_url'] = featured_image_url
        
        return mars_info
    
    finally:
               browser.quit() 
def scrape_mars_weather():
    try:
        browser = init_browser()
        
        url = 'https://twitter.com/marswxreport?lang=en'
        browser.visit(url)

        time.sleep(5)
        
        html = browser.html
        weather_soup = bs(html, 'html.parser')
        
        mars_weather_tweet = weather_soup.find('div', attrs={'class':
     'tweet','data-name': 'Mars Weather'})
        
        try:
            mars_weather = mars_weather_tweet.find('p', 'tweet-tex').get_text()
            mars_weather

        except AttributeError:
            
            pattern = re.compile(r'sol')
            mars_weather = weather_soup.find('span',text=pattern).text
            mars_weather
    
            mars_info['mars_weather'] = mars_weather
            return mars_info
        
    finally:
            
        browser.quit()  
def scrape_mars_facts():
    
        df = pd.read_html('https://space-facts.com/mars/')[0]
        df.columns=['Description','Value']
        
        data = df.columns.to_html()
        
        mars_info['df.columns'] = data
        return mars_info
def scrape_mars_hemispheres():
    try:
        browser = init_browser()
        
        url ='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url)
        
        hemisphere_image_urls = []
        links = browser.find_by_css('a.product-item h3')

        for i in range(len(links)):
             hemisphere = {}
    
             browser.find_by_css('a.product-item h3')[i].click()
             sample_elem = browser.find_link_by_text('Sample').first
             hemisphere['img_url'] = sample_elem['href']
    
             hemisphere['title'] = browser.find_by_css('h2.title').text
    
             hemisphere_image_urls.append(hemisphere)
    
             browser.back()
        
             hemisphere_image_urls.append({"title","img_url"})
             
        mars_info['hemisphere_image_urls'] = hemisphere_image_urls
        
        return mars_info
   
    finally:
         
        browser.quit()    
                        