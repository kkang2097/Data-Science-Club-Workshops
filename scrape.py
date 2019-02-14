# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 13:12:51 2019

@author: Elliot
"""

import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Chrome/70.0.3538.77'}

url = "https://radio-locator.com/info/WANM-FM"
#headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}

r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.text, 'html.parser')
print(soup.prettify())

#Parsing URL to real website
soup.p.a.text

#Parsing phone number
#Regex for it: (?:1[-.])*(?[2-9]\d{2})?[-. ]\d{3}[-. ]\d{4}
import re
r.text
every = re.findall(r'\d{3}-\d{3}-\d{4}', r.text)
print(every[0])


'''

Dynamic Website Example

Borrowed from YouTube
https://www.youtube.com/watch?v=4o2Eas2WqAQ


'''
string = 'Hellowerewk'
print(f"sldfjaskf {string}")


from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from bs4 import BeautifulSoup
import urllib.request


class CraiglistScraper(object):
    def __init__(self, location, postal, max_price, radius):
        self.location = location
        self.postal = postal
        self.max_price = max_price
        self.radius = radius

        self.url = f"https://{location}.craigslist.org/search/sss?search_distance={radius}&postal={postal}&max_price={max_price}"
    
        self.driver = webdriver.Chrome()
        self.delay = 3

    def load_craigslist_url(self):
        self.driver.get(self.url)
        try:
            wait = WebDriverWait(self.driver, self.delay)
            wait.until(EC.presence_of_element_located((By.ID, "searchform")))
            print("Page is ready")
        except TimeoutException:
            print("Loading took too much time")

    def extract_post_information(self):
        all_posts = self.driver.find_elements_by_class_name("result-row")

        dates = []
        titles = []
        prices = []

        for post in all_posts:
            title = post.text.split("$")

            if title[0] == '':
                title = title[1]
            else:
                title = title[0]

            title = title.split("\n")
            price = title[0]
            title = title[-1]

            title = title.split(" ")

            month = title[0]
            day = title[1]
            title = ' '.join(title[2:])
            date = month + " " + day

            #print("PRICE: " + price)
            #print("TITLE: " + title)
            #print("DATE: " + date)

            titles.append(title)
            prices.append(price)
            dates.append(date)

        return titles, prices, dates

    def extract_post_urls(self):
        url_list = []
        html_page = urllib.request.urlopen(self.url)
        soup = BeautifulSoup(html_page, "lxml")
        for link in soup.findAll("a", {"class": "result-title hdrlnk"}):
            print(link["href"])
            url_list.append(link["href"])
        return url_list

    def quit(self):
        self.driver.close()


location = "sfbay"
postal = "94201"
max_price = "500"
radius = "5"

scraper = CraiglistScraper(location = location, postal = postal, max_price = max_price, radius = radius)
scraper.load_craigslist_url()
titles, prices, dates = scraper.extract_post_information()
print(titles)
#scraper.extract_post_urls()
#scraper.quit()


'''

Infinitely scrolling pages

'''

import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

browser = webdriver.PhantomJS("phantomjs")
browser.get("https://twitter.com/StackStatus")
print(browser.title)

pause = 3

lastHeight = browser.execute_script("return document.body.scrollHeight")
print(lastHeight)
i = 0

while True:
	browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	time.sleep(pause)
	newHeight = browser.execute_script("return document.body.scrollHeight")
	print(newHeight)
	if newHeight == lastHeight:
        #Insert web scraping here
        print("End of page")
		break
	lastHeight = newHeight
	i += 1
