import os
import re
import time

import requests
from bs4 import BeautifulSoup, Comment
from requests.exceptions import ConnectionError
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def first_query_page():
    #Access the main search page of the law precedent system
    #driver download: https://googlechromelabs.github.io/chrome-for-testing/
    #In the latest version of Selenium, webdriver is no longer needed to be downloaded
    #https://stackoverflow.com/questions/76550506/typeerror-webdriver-init-got-an-unexpected-keyword-argument-executable-p
    driver = webdriver.Chrome()
    url = "https://judgment.judicial.gov.tw/FJUD/Default_AD.aspx
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
    content.send_keys(31)
    driver.find_element("name", "ctl00$cp_content$btnQry").click()

    # retrieve page of query result
    handles = driver.window_handles
    driver.switch_to.window(handles[-1])
    time.sleep(0.5)

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


content = get_bs4_content(url=first_query_page())
