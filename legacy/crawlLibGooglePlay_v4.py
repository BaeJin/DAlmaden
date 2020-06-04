from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException

import sys
import time
from datetime import datetime
from bs4 import BeautifulSoup
import requests, pymysql
import re


class GooglePlayCrawler:

    def __init__(self, keyword, channel):
        self.keyword = keyword
        self.channel = channel

        
    def cleanse(self, text):

        text = re.sub('[,#/$.@*\"※&%ㆍ』\\‘|\(\)\[\]\<\>`\'…》]', '', text)

        text = re.sub(r'\\', '', text)
        text = re.sub(r'\\\\', '', text)
        text = re.sub('\'', '', text)
        text = re.sub('\"', '', text)

        text = re.sub('\u200b', ' ', text)
        text = re.sub('&nbsp;|\t', ' ', text)
        text = re.sub('\r\n', '\n', text)

        while (True):
            text = re.sub('  ', ' ', text)
            if text.count('  ') == 0:
                break

        while (True):
            text = re.sub('\n \n ', '\n', text)
            # print(text.count('\n \n '))
            if text.count('\n \n ') == 0:
                break

        while (True):
            text = re.sub(' \n', '\n', text)
            if text.count(' \n') == 0:
                break

        while (True):
            text = re.sub('\n ', '\n', text)
            if text.count('\n ') == 0:
                break

        while (True):
            text = re.sub('\n\n', '\n', text)
            # print(text.count('\n\n'))
            if text.count('\n\n') == 0:
                break
        text = re.sub(u'[\u2500-\u2BEF]', '', text)  # I changed this to exclude chinese char

        # dingbats
        text = re.sub('\[-|\]|\{|\}|\(|\)', "", text)

        text = re.sub(u'[\u2702-\u27b0]', '', text)
        text = re.sub(u'[\uD800-\uDFFF]', '', text)
        text = re.sub(u'[\U0001F600-\U0001F64F]', '', text)  # emoticons
        text = re.sub(u'[\U0001F300-\U0001F5FF]', '', text)  # symbols & pictographs
        text = re.sub(u'[\U0001F680-\U0001F6FF]', '', text)  # transport & map symbols
        text = re.sub(u'[\U0001F1E0-\U0001F1FF]', '', text)  # flags (iOS)
        text = re.sub(u'[\u2500-\u2BEF]', '', text)  # I changed this to exclude chinese char

        # dingbats
        text = re.sub(u'[\u2702-\u27b0]', '', text)

        text = re.sub(u'[\uD800-\uDFFF]', '', text)
        text = re.sub(u'[\U0001F600-\U0001F64F]', '', text)  # emoticons
        text = re.sub(u'[\U0001F300-\U0001F5FF]', '', text)  # symbols & pictographs
        text = re.sub(u'[\U0001F680-\U0001F6FF]', '', text)  # transport & map symbols
        text = re.sub(u'[\U0001F1E0-\U0001F1FF]', '', text)  # flags (iOS)

        text = re.sub(u'[\'\"\%\?]', '', text)

        # text = re.sub(u'[\U0001F600-\U0001F1FF]', '', text)

        return text

    
    def crawlReviews(self):
        
        #getting all_reviews page for wanted application

        

##        url = "https://play.google.com/store/search?q=%s"%(self.keyword)
##        response1 = requests.get(url)
##        response1 = response1.text
##        soup1 = BeautifulSoup(response1,"lxml")
##        x = soup1.find('a',class_='poRVub')
##        target_url = x.attrs['href']
##        target_url = 'https://play.google.com'+target_url
##        print(target_url)
        
        options = Options()
        options.headless = True
        driver = webdriver.Firefox(options=options)
        #driver = webdriver.Firefox()
        url = "https://play.google.com/store/search?q="+self.keyword+"&c=apps"
        driver.get(url)
        time.sleep(2)
        driver.implicitly_wait(3)
        print("Headless Firefox Initialized")

        find_app = driver.find_elements_by_xpath("//div[@class='WsMG1c nnK0zc']")
        for f in find_app:
            if f.text == self.keyword:
                wanted_app = f
        wanted_app.click()
        time.sleep(4)
        driver.implicitly_wait(5)
        currentUrl = driver.current_url
        wanted_url = currentUrl + "&showAllReviews=true"
        driver.get(wanted_url)
        driver.implicitly_wait(3)
        time.sleep(2)

        i = 0
        Usermemory = []
        Reviewmemory = []
        #getting info
        
        
        while True:
            k = 0
            while k <= 30:
            
                last_height = driver.execute_script("return document.documentElement.scrollHeight")
                print("\n\n\nNEXT PAGE**************\n\n\n");
                driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
                time.sleep(1.5)
                driver.implicitly_wait(3)
                new_height = driver.execute_script("return document.documentElement.scrollHeight")
                if new_height == last_height:
                     try:
                        morereviews = driver.find_element_by_xpath(
                            "//span[@class='CwaK9']/span[@class='RveJvd snByac']")
                        morereviews.click()
                        driver.implicitly_wait(1)
                     except:
                        break
                last_height = new_height
                k = k+1
                
            try:
                whole_review = driver.find_elements_by_xpath("//button[@class='LkLjZd ScJHi OzU4dc  ']")
                for w in whole_review:
                    w.click()
                    driver.implicitly_wait(1)
            except:
                print("whole_review is shown")

            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            time.sleep(2)

            UsernameList = []
            StarList = []
            LikeList = []
            DatetimeList = []
            ReviewList = []

            #try:
            
            if len(Usermemory) == 0:
                htm = driver.find_elements_by_xpath("//div[@class='d15Mdf bAhLNe']")
                print("Initiating...")
                for ahtm in htm:
                                
                    html = ahtm.get_attribute("outerHTML")
                    soup = BeautifulSoup(html, "lxml")
                    print("reading: "+str(len(htm))+" reviews.")
                    try:
                        username = soup.find('span',{'class':'X43Kjb'}).text
                        #print(username)
                        cuser = self.cleanse(username)
                        UsernameList.append(cuser)
                        Usermemory.append(username)
                        print("getting " + cuser +"'s review")

                        s_1 = soup.find('div',{'class':'pf5lIe'})
                        star = str(s_1)[47]
                        #print(star)
                        StarList.append(star)

                        d_1 = soup.find('span',{'class':'p2TkOb'}).text
                        a = d_1.replace('년 ', '-')
                        b = a.replace('월 ', '-')
                        date = b.replace('일', '')
                        #print(date)
                        DatetimeList.append(date)

                        like = soup.find('div',{'class':'jUL89d y92BAb'}).text
                        #print(l_1)
                        LikeList.append(like)

                        r_1 = soup.find('span',{'jsname':'fbQN7e'}).text

                        if r_1 is '':
                            r_0 = soup.find('span',{'jsname':'bN97Pc'}).text
                            review_0 = self.cleanse(r_0)
                            ReviewList.append(review_0)
                            Reviewmemory.append(r_0)
                            #print(r_0)
                        else:
                            review_1 = self.cleanse(r_1)
                            ReviewList.append(review_1)
                            Reviewmemory.append(r_1)
                            #print(r_1)
                   
                    
                    except Exception as e:
                        print('error',e)

            else:
                last_username = Usermemory[-1]
                last_review = Reviewmemory[-1]
                y=-2
                #print(last_username)
                #print(last_review)
                while True:
                    try:
                        userbox_0 = driver.find_elements_by_xpath("//span[text() = '"+str(last_username)+"']")
                        driver.implicitly_wait(10)
                        print(len(userbox_0))
                        for u in userbox_0:
                            print("currently crawled: "+str(len(Usermemory)))
                            userbox_1 = u.find_element_by_xpath("ancestor::div[@jscontroller='H6eOGe']")
                            #textbox_0 = userbox_1.find_element_by_xpath(".//span[text() = '"+str(last_review)+"']")
                            textbox_0 = userbox_1.find_element_by_xpath(".//span[@jsname = 'bN97Pc']")
                            if textbox_0.text == '':
                                textbox_0 = userbox_1.find_element_by_xpath(".//span[@jsname='fbQN7e']")
                                print("This review is long")
                            else:
                                print("This review is short")
                            print("found corresponding review")
                            if str(last_username)+str(last_review) == str(u.text)+str(textbox_0.text):
                                sibling = userbox_1.find_elements_by_xpath("following-sibling::div[@jscontroller='H6eOGe']")
                                print("found: "+str(len(sibling))+" siblings")
                                for sis in sibling:
                                    try:
                                        ahtm = sis.find_element_by_xpath(".//div[@class='d15Mdf bAhLNe']")
                                        driver.implicitly_wait(1)
                                        html = ahtm.get_attribute("outerHTML")
                                        soup = BeautifulSoup(html, "lxml")
                                        print("reading: "+str(len(sibling))+" reviews.")
                                        print("currently crawled: "+str(len(Usermemory)))
                                        
                                        username = soup.find('span',{'class':'X43Kjb'}).text
                                        #print(username)
                                        cuser = self.cleanse(username)
                                        UsernameList.append(cuser)
                                        Usermemory.append(username)
                                        print("getting " + cuser +"'s review")

                                        s_1 = soup.find('div',{'class':'pf5lIe'})
                                        star = str(s_1)[47]
                                        #print(star)
                                        StarList.append(star)

                                        d_1 = soup.find('span',{'class':'p2TkOb'}).text
                                        a = d_1.replace('년 ', '-')
                                        b = a.replace('월 ', '-')
                                        date = b.replace('일', '')
                                        #print(date)
                                        DatetimeList.append(date)

                                        like = soup.find('div',{'class':'jUL89d y92BAb'}).text
                                        #print(l_1)
                                        LikeList.append(like)

                                        r_1 = soup.find('span',{'jsname':'fbQN7e'}).text

                                        if r_1 is '':
                                            r_0 = soup.find('span',{'jsname':'bN97Pc'}).text
                                            review_0 = self.cleanse(r_0)
                                            ReviewList.append(review_0)
                                            Reviewmemory.append(r_0)
                                            #print(r_0)
                                        else:
                                            review_1 = self.cleanse(r_1)
                                            ReviewList.append(review_1)
                                            Reviewmemory.append(r_1)
                                            #print(r_1)
                                   
                                    
                                    except Exception as e:
                                        print('error',e)
                                        continue
                    
                                
                                break
                            else:
                                print("failed to find current node..searching again")
                                #print(u.text)
                                #print(textbox_0.text)
                                continue
                        if (len(userbox_0) ==1 and str(last_username)+str(last_review) != str(u.text)+str(textbox_0.text)):
                            last_username = Usermemory[y]
                            last_review = Reviewmemory[y]
                            y-=1
                            
                        else:
                            if len(UsernameList)==0:
                                last_username = Usermemory[y]
                                last_review = Reviewmemory[y]
                                y-=1
                            else:
                                break
                    except:
                        print("error")
                        time.sleep(120)
                        
                    


            
           
                
                
            #except:
                #print("error occured while getting reviews..I will sleep for 2 minutes")
                #time.sleep(120)

            #print(UsernameList)
            print(len(UsernameList))
            #print(StarList)
            print(len(StarList))
            #print(LikeList)
            print(len(LikeList))
            #print(DatetimeList)
            print(len(DatetimeList))
            #print(ReviewList, sep = "\n")
            print(len(ReviewList))
            
            
            
            
            dtNow = datetime.now()
            dtStr = dtNow.strftime("%Y-%m-%d %H:%M:%S")

            ##DB##
            conn = pymysql.connect(host='106.246.169.202', user='root', password='robot369',
                                   db='crawl2', charset='utf8mb4')
            curs = conn.cursor(pymysql.cursors.DictCursor)
            for a, b, c, d, e in zip(UsernameList, StarList, DatetimeList, LikeList, ReviewList):
                try:
                    
                    sql0 = "select count(*) from scrapying where keyword = \'%s\' and username = \'%s\' and review = \'%s\'" % (self.keyword, a, e)
                    curs.execute(sql0)
                    n_check = curs.fetchall()
                    if n_check[0]['count(*)'] == 0:
                        sql = "insert into scrapying(keyword,channel, accesstime, username, star_rating, date, slike, review, role) " \
                          + "values (\'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\',\'%s\', \'%s\', \'%s\')" % \
                          (self.keyword, self.channel, dtStr, a, b, c, d, e, 'review')
                        curs.execute(sql)
                except:
                    print("sql error")
                    continue
                conn.commit()
            conn.close()


            
            try:
                i = 0
                while i <= 3:
                    last_height = driver.execute_script("return document.documentElement.scrollHeight")
                    print("\n\n\nNEXT PAGE**************\n\n\n");
                    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
                    time.sleep(1.5)
                    driver.implicitly_wait(3)
                    new_height = driver.execute_script("return document.documentElement.scrollHeight")
                    if new_height == last_height:
                        break
                    last_height = new_height
                    i = i+1
                
                morereviews = driver.find_element_by_xpath("//span[@class='CwaK9']/span[@class='RveJvd snByac']")
                morereviews.click()
                driver.implicitly_wait(1)
            
            except:
                break
        print("completed crawling")
        print("crawled: "+str(len(Usermemory)) +" reviews")
        driver.quit()
        
