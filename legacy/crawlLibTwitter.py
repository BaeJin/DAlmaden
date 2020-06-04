from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

import sys
import time
from datetime import datetime
from bs4 import BeautifulSoup
import requests, pymysql
import re
from selenium.webdriver.common.keys import Keys

class TwitterLister:

    def __init__(self, nUrl, keyword, channel, startDate, endDate):
        self.nUrl = nUrl
        self.keyword = keyword
        self.channel = channel
        self.startDate = startDate
        self.endDate = endDate


    def getTwitterUrl(self):
        ##openpage##
        url = 'https://twitter.com'
        driver=webdriver.Firefox()

        driver.get(url)
        driver.implicitly_wait(5)


        ##login##
        putid=driver.find_element_by_xpath("//input[@class='text-input email-input js-signin-email']")
        putid.send_keys('01035178914')
        time.sleep(2)
        putpassword=driver.find_element_by_xpath("//input[@class='text-input']")
        putpassword.send_keys('robot369')
        time.sleep(2)
        login=driver.find_element_by_xpath("//input[@class='EdgeButton EdgeButton--secondary EdgeButton--medium submit js-submit']")
        login.click()
        time.sleep(5)


        ##search##
        findsearchbox=driver.find_element_by_xpath("//input[@class='r-30o5oe r-1niwhzg r-17gur6a r-1yadl64 r-deolkf r-homxoj r-poiln3 r-7cikom r-1ny4l3l r-1sp51qo r-1lrr6ok r-1dz5y72 r-1ttztb7 r-13qz1uu']")
        findsearchbox.send_keys(self.keyword+" until:"+self.endDate+" since:"+self.startDate)
        time.sleep(1)
        findsearchbox.send_keys('\ue007')
        time.sleep(5)


        UrlList=[]
        TimeList=[]
        pgLoc = -1.0
        while True:
            try:
                gethrefelem=driver.find_elements_by_xpath("//a[@class='css-4rbku5 css-18t94o4 css-901oao r-1re7ezh r-1loqt21 r-1q142lx r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-3s2u2q r-qvutc0']")
                for hrefelem in gethrefelem:
                    href=hrefelem.get_attribute('href')
                    gettimeelem=hrefelem.find_element_by_css_selector('time')
                    a = gettimeelem.get_attribute("datetime")
                    b=a.split('.')
                    c=b[0].split('T')
                    dtime=c[0]+' '+c[1]
                    print(href)
                    print(dtime)
                    if href not in UrlList:
                        UrlList.append(href)
                        TimeList.append(dtime)

                body = driver.find_element_by_css_selector('body')
                body.send_keys(Keys.PAGE_DOWN)

                time.sleep(1)

                prevLoc=pgLoc
                pgLoc = driver.execute_script("return window.pageYOffset;");
                print("Page location = ", pgLoc)
                if pgLoc==prevLoc:
                    break
                if (len(UrlList) >= self.nUrl):
                    break
            except:
                print("driver picking up stale element")

        print(*UrlList, sep = "\n")
        print(*TimeList, sep = "\n")
        print(len(UrlList))
        print(len(TimeList))
        print("\n\n\nEND OF SCROLL*****************\n\n\n");




        ##DBUpdate##

        dtNow = datetime.now()
        dtStr = dtNow.strftime("%Y-%m-%d %H:%M:%S")

        conn = pymysql.connect(host='106.246.169.202', user='root', password='robot369',
                                       db='crawl', charset='utf8mb4')
        curs = conn.cursor()



        for Url, publishTime in zip(UrlList, TimeList):
            sql0 = "select * from urllist where url=\'" + Url + "\' " \
                                   + "and keyword=\'"+self.keyword+"\' "\
                                   + "and publishtime=\'%s\'"%(publishTime)
            curs.execute(sql0)
            rows = curs.fetchall()
            if len(rows)==0:
         
          
                sql = "insert into urllist(keyword, channel, stdate, endate, accesstime, url, publishtime, crawled) " \
                              + "values (\'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\',  \'%s\', \'%s\')" % \
                              (self.keyword, self.channel, self.startDate, self.endDate, dtStr, Url, publishTime, 'F')
                curs.execute(sql)
                conn.commit()

        conn.close()

        driver.close()

class TwitterCrawler:

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
        text = re.sub(u'[\u2500-\u2BEF]', '', text) # I changed this to exclude chinese char

  
        #dingbats
        text = re.sub(u'[\u2702-\u27b0]', '', text)

        text = re.sub(u'[\uD800-\uDFFF]', '', text)
        text = re.sub(u'[\U0001F600-\U0001F64F]', '', text) # emoticons
        text = re.sub(u'[\U0001F300-\U0001F5FF]', '', text) # symbols & pictographs
        text = re.sub(u'[\U0001F680-\U0001F6FF]', '', text) # transport & map symbols
        text = re.sub(u'[\U0001F1E0-\U0001F1FF]', '', text) # flags (iOS)

        text = re.sub(u'[\'\"\%\?]', '', text)
        
        #text = re.sub(u'[\U0001F600-\U0001F1FF]', '', text)

        return text


    def crawlUrlTexts(self):
        driver = webdriver.Firefox()
        ###login###
        homeurl = 'https://twitter.com'
        driver.get(homeurl)
        driver.implicitly_wait(5)

        putid=driver.find_element_by_xpath("//input[@class='text-input email-input js-signin-email']")
        putid.send_keys('01035178914')
        time.sleep(2)
        putpassword=driver.find_element_by_xpath("//input[@class='text-input']")
        putpassword.send_keys('robot369')
        time.sleep(2)
        login=driver.find_element_by_xpath("//input[@class='EdgeButton EdgeButton--secondary EdgeButton--medium submit js-submit']")
        login.click()
        time.sleep(5)
        ###get url from DB###
        conn = pymysql.connect(host='106.246.169.202', user='root', password='robot369',
                                       db='crawl', charset='utf8mb4')
        curs = conn.cursor(pymysql.cursors.DictCursor)

        sql = "select * from urllist where keyword=\'%s\' and channel=\'%s\' and crawled=\'%s\'" % \
              (self.keyword, self.channel, 'F')

        print(sql)
        curs.execute(sql)

        rows = curs.fetchall()
        print("Total %s urls targeted..."%(len(rows)))

        
        print(rows)
        
        for row in rows:
            url = row['url']
            now = datetime.now()
            dtStr = now.strftime("%Y-%m-%d %H:%M:%S")
        #get url
            driver.get(url)
            driver.implicitly_wait(3)
            time.sleep(5)

            comments = []
            pubtimelist = []
            publishtime = []
            pgLoc = -1.0
            i = 1
            driver.implicitly_wait(0.5)
            while True:
                try:
                    ###get pubtime and comments###
                    print("===========================")
                    print("reached here")


                    ht = driver.find_element_by_xpath("//div[@style='padding-bottom: 0px;']/div")
                    print(ht.get_attribute('style'))
                    while True:
                        try:
                            clckcomments = ht.find_element_by_xpath(".//div[@class='css-901oao r-1n1174f r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-qvutc0']/span[@class='css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0']")
                            clckcomments.click()
                        except:
                            break
                    #articleInfo = ht.find_element_by_xpath("./div/div/article//div[@class='css-901oao r-hkyrab r-1qd0xha r-1blvdjr r-16dba41 r-ad9z0x r-bcqeeo r-19yat4t r-bnwqim r-qvutc0']")
                    if i==1: 
                        articleInfo = ht.find_element_by_xpath(".//div[@class='css-901oao r-hkyrab r-1qd0xha r-1blvdjr r-16dba41 r-ad9z0x r-bcqeeo r-19yat4t r-bnwqim r-qvutc0']")
                        print(articleInfo.text)
                        AI = articleInfo.text
                        articleT = self.cleanse(AI)
                    #replyInfo = ht.find_elements_by_xpath(".//div[@class='css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0']")
                    replybox = ht.find_elements_by_xpath(".//article[@class='css-1dbjc4n r-1loqt21 r-1udh08x r-o7ynqc r-1j63xyz']")
                    for rb in replybox:
                        try:
                            replyInfo = rb.find_element_by_xpath(".//div[starts-with(@class, 'css-901oao r-hkyrab') and contains(@class, 'r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0')]")
                            rDT = rb.find_element_by_xpath(".//time[@datetime]")
                            rD = rDT.get_attribute('datetime')
                            if replyInfo.text not in comments:
                                comments.append(replyInfo.text)
                                print(replyInfo.text)
                                b=rD.split('.')
                                c=b[0].split('T')
                                dtime=c[0]+' '+c[1]
                                publishtime.append(dtime)
                                print(dtime)
                        except:
                            continue

                    i+=1

                    body = driver.find_element_by_css_selector('body')
                    body.send_keys(Keys.PAGE_DOWN)

                    time.sleep(0.5)

                    prevLoc=pgLoc
                    pgLoc = driver.execute_script("return window.pageYOffset;");
                    print("Page location = ", pgLoc)
                    if pgLoc==prevLoc:
                        try:
                            showmorerep=driver.find_element_by_xpath("//div[@class='css-1dbjc4n r-my5ep6 r-qklmqi r-1adg3ll']/div/div/div/span[@class='css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0']")
                            showmorerep.click()
                        except:
                            break
                except:
                    articleInfo = driver.find_element_by_xpath("//div[@class='css-901oao r-hkyrab r-1qd0xha r-1blvdjr r-16dba41 r-ad9z0x r-bcqeeo r-19yat4t r-bnwqim r-qvutc0']")
                    print(articleInfo.text)
                    AI = articleInfo.text
                    articleT = self.cleanse(AI)
                    break


            print(*comments, sep = '\n')
            print(*publishtime, sep = '\n')
            print(len(comments))
            print(len(publishtime))
            
            
            sql = "insert into htdocs(keyword, channel, url, accesstime, htmltext, role)" \
                              + "values (\'%s\', \'%s\', \'%s\', \'%s\',\'%s\', \'%s\')" % \
                              (self.keyword, self.channel, url, dtStr, articleT, 'article')
            
            curs.execute(sql)
            conn.commit()
 

            for c, p in zip(comments,publishtime):
                cText=self.cleanse(c)
                if len(cText) !=0:
                    sql = "insert into htdocs(keyword, channel, url, accesstime, publishtime, htmltext, role)" \
                          + "values (\'%s\', \'%s\', \'%s\',\'%s\', \'%s\', \'%s\', \'%s\')" % \
                          (self.keyword, self.channel, url, dtStr, p, cText, 'comment')
                    curs.execute(sql)
            conn.commit()

        ###updatepubtime###
            try:
                sqlu = "update urllist set crawled=\'T\', crawltime=\'%s\' where keyword=\'%s\' and url=\'%s\'" %(dtStr, self.keyword, url)
                curs.execute(sqlu)
                sqli = "select * from urllist where keyword =\'%s\' and url=\'%s\'"%(self.keyword, url)
                curs.execute(sqli)
                rows2 = curs.fetchall()
                rowp = rows2['publishtime']
                sqlk = "update htdocs set publishtime=\'%s\' where keyword=\'%s\' and url=\'%s\' and role = 'article'" %(rowp, self.keyword, url)
                conn.commit()
            except:
                continue

        conn.close()


