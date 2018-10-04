import pandas as pd
import requests
import time
from splinter import Browser
from bs4 import BeautifulSoup
from datetime import datetime
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

mars_things = {}
url = 'https://mars.nasa.gov/news/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
#print(soup.prettify())

news_title = soup.find('div', class_='content_title').text
news_p = soup.find('div', class_='rollover_description_inner').text
#print(news_title)
#print(news_p)

mars_things['news_title'] = news_title
mars_things['news_p'] = news_p
#mars_things

executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)
imagesurl = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(imagesurl)
browser.click_link_by_partial_text('FULL IMAGE')
time.sleep(10)
browser.click_link_by_partial_text('more info')
time.sleep(5)
html = browser.html
imagesoup = BeautifulSoup(html, 'html.parser')
image = imagesoup.find('figure', class_='lede')
#image

link = image.a['href']
#link

featured_image_url = 'https://www.jpl.nasa.gov' + link
#featured_image_url

mars_things['featured_image_url'] = featured_image_url
#mars_things

mars_twitter_url = 'https://twitter.com/marswxreport?lang=en'
response_weather = requests.get(mars_twitter_url)

soup_weather = BeautifulSoup(response_weather.text, 'lxml')
mars_weather = soup_weather.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
#print(mars_weather)
mars_things['mars_weather']=mars_weather

mars_facts_url='https://space-facts.com/mars/'
mars_facts=pd.read_html(mars_facts_url)
mars_facts=mars_facts[0].rename(columns={0:'description', 1:'value'})
mars_facts=mars_facts.set_index('description')
mars_facts_html=mars_facts.to_html()
#print(mars_facts)
mars_things['mars_facts_html']=mars_facts_html

mars_hemi_url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
response_hemi = requests.get(mars_hemi_url)

soup_hemi = BeautifulSoup(response_hemi.text, 'lxml')
mars_hemis=soup_hemi.find_all('a', class_="item product-item")
hemi_titles=[]
for hemi in mars_hemis:
    title=hemi.find('h3').text
    link=hemi['href']
    hemi_titles.append(title)
    print(title)
    print(link)
executable_path = {'executable_path': 'chromedriver'}
browser = Browser('chrome', **executable_path)
browser.visit(mars_hemi_url)
hemisphere_image_urls = []
for i in range(len(hemi_titles)):
    try:
        browser.click_link_by_partial_text(hemi_titles[i])
    except:
        browser.find_link_by_text('2').first.click()
        browser.click_link_by_partial_text(hemi_titles[i])
    html = browser.html
    soup3 = BeautifulSoup(html, 'html.parser')
        
    hemi_downloads = soup3.find('div', 'downloads')
    print(hemi_titles[i], i, '-------------')
    hemi_url=hemi_downloads.a['href']
    print(hemi_url)
    hemi_dict={"title": hemi_titles[i], 'img_url': hemi_url}
    hemisphere_image_urls.append(hemi_dict)
mars_things['hemisphere_image_urls'] = hemisphere_image_urls

return mars_things