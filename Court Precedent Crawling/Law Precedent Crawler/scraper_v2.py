import time
import configparser
import logging
import os
import re
import sys
import time
from datetime import date

import pandas as pd
import urllib3
import xlsxwriter

import requests
from bs4 import BeautifulSoup, Comment
from requests.exceptions import ConnectionError
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Add custom user-agent to prevent blocking
#from selenium.webdriver.chrome.options import Options
#from fake_useragent import UserAgent

#ua = UserAgent()
#chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument(f'--user-agent={ua.random}')


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def first_query_page():
    #Access the main search page of the law precedent system
    #driver download: https://googlechromelabs.github.io/chrome-for-testing/
    #In the latest version of Selenium, webdriver is no longer needed to be downloaded
    #https://stackoverflow.com/questions/76550506/typeerror-webdriver-init-got-an-unexpected-keyword-argument-executable-p
    #driver = webdriver.Chrome(options=chrome_options)
    driver = webdriver.Chrome()
    url = "https://judgment.judicial.gov.tw/FJUD/Default_AD.aspx"
    driver.get(url)

    #Find the elements and simulate the clicks

    #Type of precendent
    #find_element function is changed
    #https://stackoverflow.com/questions/72773206/selenium-python-attributeerror-webdriver-object-has-no-attribute-find-el
    driver.find_element(By.XPATH, "//*[@id='vtype_M']/input").click()
    #Date range start
    content = driver.find_element("name", "dy1")
    content.send_keys(113)
    content = driver.find_element("name", "dm1")
    content.send_keys(7)
    content = driver.find_element("name", "dd1")
    content.send_keys(16)
    #Date range end
    content = driver.find_element("name", "dy2")
    content.send_keys(113)
    content = driver.find_element("name", "dm2")
    content.send_keys(7)
    content = driver.find_element("name", "dd2")
    content.send_keys(30)
    #Select the court
    driver.find_element(By.XPATH, "//*[@id='jud_court']/option[22]").click()
    #Click the search button
    driver.find_element("name", "ctl00$cp_content$btnQry").click()



    # Fetch all the URLs of the query result
    # Should use a for loop to automate saving all the URLs for the individual data page

    #Switch frame (Very important for dynamic load with iframes or others)
    #https://ithelp.ithome.com.tw/articles/10269242
    #https://selenium-python.readthedocs.io/api.html
    driver.switch_to.frame("iframe-data")
    
    
    # Wait for the page to load
    #WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'hlTitle')))
    #WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'hlTitle')))
    time.sleep(3)

    # Extract the page source
    page_source = driver.page_source
    #page_source = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")

    # Parse the page source with BeautifulSoup
    source_soup = BeautifulSoup(page_source, 'html.parser')
    page_content = source_soup
    print(page_content)

    #Conditioned article URL fetch (Some URL are None)
    article_URLs = []
    for node in page_content.find_all("a", id="hlTitle"):
        if node.get("href") is not None:
            article_URLs.append(f'https://judgment.judicial.gov.tw/FJUD/{node.get("href")}')
        else:
            pass
    

    print(article_URLs)
    print(len(article_URLs))
    #print(type(article_URLs))


    # retrieve page of query result
    handles = driver.window_handles
    driver.switch_to.window(handles[-1])
    time.sleep(5)

    # switch to the page
    page_url = driver.current_url
    return page_url



def get_bs4_content(url):
    res = requests.get(url, verify=False)
    soup = BeautifulSoup(res.text, "html.parser")
    return soup


def get_main_text(content):
    raw_text = content.find("body").find(
        "div", {"class": "text-pre text-pre-in"})
    sentences = raw_text.find_all(
        text=lambda text: isinstance(text, Comment))
    main_text = ",".join(sentences)
    return main_text


def get_full_text(content):
    nodes = content.find("body").find_all("td")
    full_text = ",".join([node.text for node in nodes])
    return full_text


#Some temp callers for testing out the selenium code
#content = get_bs4_content(url=first_query_page())
#print(first_query_page())



#Main function

first_query_page()


## https://judgment.judicial.gov.tw/FJUD/data.aspx?ty=JD&id=TPDM%2c113%2c%e8%81%b2%2c1706%2c20240730%2c1&ot=in
## https://judgment.judicial.gov.tw/FJUD/data.aspx?ty=JD&id=TPDM%2c113%2c%e8%81%b2%2c1706%2c20240730%2c1&ot=in