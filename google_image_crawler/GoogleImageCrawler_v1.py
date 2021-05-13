from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException
import os
import sys
import time
from datetime import datetime
from bs4 import BeautifulSoup
import requests, pymysql
import re

def OpenBrowser(keyword):
    ## Open driver and get Url ##
    options = Options()
    # options.headless =  True
    driver = webdriver.Firefox(options=options)
    url="https://www.google.co.kr/search?hl=ko&tbm=isch&sxsrf=ACYBGNRbe0RtwYujJ1jJ1nd-qpUWIk799A%3A1580893160634&source=hp&biw=1920&bih=966&ei=6IM6Xvb9I4ys0QTJlL6oCw&q="+keyword+"&oq="+keyword+"&gs_l=img.3...1531.4221..4318...2.0..1.105.1032.11j1......0....1..gws-wiz-img.....10..35i39j0j35i362i39j0i131.R3i9kaayoeY&ved=0ahUKEwj2kY_6hbrnAhUMVpQKHUmKD7UQ4dUDCAU&uact=5"
    driver.get(url)
    time.sleep(2)
    driver.implicitly_wait(3)
    print("Headless Firefox Initialized")

def ScrollDown(): 
    while True:
        last_height = driver.execute_script("return document.documentElement.scrollHeight")
        print("\n\n\nScroll_Down**************\n\n\n")
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight)")
        time.sleep(2)
        driver.implicitly_wait(3)
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            try:
                more_images = driver.find_element_by_xpath("//input[@class='mye4qd']")
                more_images.click()
                driver.implicitly_wait(1)
            except:
                break

def ImageUrl(x):
    data_iurl_list=[]
    data_src_list=[]
    src_list=[]
    all_list=[]
    
    for f in x:
        get_data_iurl=f.get_attribute('data-iurl')
        if get_data_iurl is not None:
            data_iurl_list.append(get_data_iurl)
        else:
            get_data_src=f.get_attribute('data-src')
            if get_data_src is not None:
                data_src_list.append(get_data_src)
            else:
                get_src=f.get_attribute('src')
                src_list.append(get_src)

    all_list = data_iurl_list + data_src_list + src_list
    print(len(all_list))
    return all_list

def ImageDownload(keyword, all_list):
  ## Check if img folder already exists ##
    image_already_in=[]
    directory = './'+keyword
    if not os.path.exists(directory):
        os.mkdir(directory)
        print("Directory " , keyword+" folder" ,  " Created ")
    else:    
        print("Directory " , keyword+" folder" ,  " already exists")
        image_file_list = os.listdir(directory)
        for item in image_file_list:        ## Check if img already exists in folder ##
            item = item.split('___1531')
            item = item[1].split('.jpg')
            item = item[0]
            image_already_in.append(item)
    v = len(image_already_in)

    ## Download img ##
    current_num = 0
    for item in all_list:
        try:
            r = requests.get(item)
            item = item.split('%3AANd9Gc')
            item = item[1]
            if item not in image_already_in:
                print("Downloading: "+item)
                filename = str(keyword +str(v)+"___1531"+item+'.jpg')
                with open('./'+keyword+'/'+filename,'wb') as f:
                    f.write(r.content)
                time.sleep(0.1)
                v+=1
                current_num+=1
                if int(current_num) >= int(wanted_num):
                    break

            else:
                print("This image already exists")
                time.sleep(0.1)

        except:
            continue
    return current_num

########################################################################


keyword = sys.argv[1]
wanted_num = sys.argv[2]  # crawls more than wanted_num #

# keyword = '고추'
# wanted_num = 1000  # crawls more than wanted_num #
#########################################################################

## Open driver and get Url ##
options = Options()
driver = webdriver.Firefox(options=options)
url="https://www.google.co.kr/search?hl=ko&tbm=isch&sxsrf=ACYBGNRbe0RtwYujJ1jJ1nd-qpUWIk799A%3A1580893160634&source=hp&biw=1920&bih=966&ei=6IM6Xvb9I4ys0QTJlL6oCw&q="+keyword+"&oq="+keyword+"&gs_l=img.3...1531.4221..4318...2.0..1.105.1032.11j1......0....1..gws-wiz-img.....10..35i39j0j35i362i39j0i131.R3i9kaayoeY&ved=0ahUKEwj2kY_6hbrnAhUMVpQKHUmKD7UQ4dUDCAU&uact=5"
driver.get(url)
time.sleep(2)
driver.implicitly_wait(3)
print("Headless Firefox Initialized")
ScrollDown()
find_img_box = driver.find_elements_by_xpath("//img[@class='rg_i Q4LuWd']")
print(find_img_box)
all_list = ImageUrl(find_img_box)
current_num = ImageDownload(keyword, all_list)


## more image ##
hrefList = []
c = 0
if int(current_num) < int(wanted_num):
    while True:
        driver.get(url)
        time.sleep(2)
        driver.implicitly_wait(3)
        find_img_box = driver.find_elements_by_xpath("//img[@class='rg_i Q4LuWd']")
        f=find_img_box[c]
        f.click()
        driver.implicitly_wait(1)

        try:
            find_href = driver.find_element_by_xpath("//a[@class='So4Urb Sa2Wmf MIdC8d']")
            get_href = find_href.get_attribute('href')
            driver.get(get_href)
            time.sleep(2)
            driver.implicitly_wait(3)
            ScrollDown()
            find_img_box2 = driver.find_elements_by_xpath("//img[@class='rg_i Q4LuWd']")
            all_list2 = ImageUrl(find_img_box2)
            c_num=ImageDownload(keyword, all_list2)
            current_num += c_num
        except:
            print("Unable to locate element")

        if int(current_num) >= int(wanted_num):
            break
        c+=1

driver.close()
