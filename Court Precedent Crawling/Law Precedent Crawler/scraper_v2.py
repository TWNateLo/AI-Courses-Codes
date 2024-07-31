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
    driver = webdriver.Chrome(executable_path=os.path.abspath(path))
    url = "https://law.judicial.gov.tw/FJUD/default_AD.aspx"
    driver.get(url)

    #Find the elements and simulate the clicks

    #Type of precendent
    driver.find_element(By.XPATH, "//*[@id='vtype_M']/input").click()
    #Date range start
    content = driver.find_element_by_name("dy1")
    content.send_keys(113)
    content = driver.find_element_by_name("dm1")
    content.send_keys(7)
    content = driver.find_element_by_name("dd1")
    content.send_keys(16)
    #Date range end
    content = driver.find_element_by_name("dy2")
    content.send_keys(113)
    content = driver.find_element_by_name("dm2")
    content.send_keys(7)
    content = driver.find_element_by_name("dd2")
    content.send_keys(16)
    driver.find_element_by_name("ctl00$cp_content$btnQry").click()



