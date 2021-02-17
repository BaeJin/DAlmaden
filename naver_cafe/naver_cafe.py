import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
import time
from pathlib import Path
import requests
from scraper_api import ScraperAPIClient

def send_request(url):
    token = 'cpVc6rnADqmWBNZwRFjVjA'
    response = requests.get(f"https://api.proxycrawl.com/?token={token}&url={url}")
    return response

#  Install the Python Requests library:
# `pip install requests`
cwd = str(Path.cwd().parents[0])
keyword = "세븐나이츠 린"
channel = 'NaverCafe'

driver = webdriver.Chrome(executable_path=f'{cwd}/DAlmaden/chromedriver.exe')
driver.get("https://cafe.naver.com/sevenknights")
time.sleep(2)
driver.implicitly_wait(3)

select_btn = driver.find_element_by_css_selector("#gnb_login_button")
select_btn.click()
id = driver.find_element_by_css_selector("#id")
pw = driver.find_element_by_css_selector("#pw")
id.send_keys("vasana12")
pw.send_keys("xmrwodud01.")
click_btn = driver.find_element_by_css_selector("#log\.login")
click_btn.click()
search_input = driver.find_element_by_css_selector("#topLayerQueryInput")
search_input.send_keys("레볼루션")

push_btn = driver.find_element_by_css_selector("#cafe-search > form > button")
push_btn.click()
driver.switch_to.frame('cafe_main')

ass = driver.find_elements_by_xpath("//div[@class='inner_list']/a[@class='article']")
for a in ass[0:1]:
    href = a.get_attribute('href')
    driver.get(href)
    print(response.text)
