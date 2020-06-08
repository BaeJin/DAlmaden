from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import os

import sys
import time
import re
from datetime import datetime
from bs4 import BeautifulSoup
import requests, pymysql

##########################################################################



class FacebookLister:

    def __init__(self, nUrl, keyword, channel):
        self.nUrl = nUrl
        self.keyword = keyword
        self.channel = channel
        self.path = os.path.dirname(os.path.realpath(__file__))
        print(self.path)
    def getFacebookUrl(self):
        
        ###popup control###
        option = Options()

        option.add_argument("--disable-infobars")
        option.add_argument("start-maximized")
        option.add_argument("--disable-extensions")

        # Pass the argument 1 to allow and 2 to block
        option.add_experimental_option("prefs", { 
            "profile.default_content_setting_values.notifications": 2 
        })
        path = self.path+"\chromedriver.exe"
        print(path)
        driver = webdriver.Chrome(options=option, executable_path=self.path+"\chromedriver.exe")
        driver.get('https://www.facebook.com')


        ##login##
        try:
            putid=driver.find_element_by_xpath("//input[@id='email']")
            driver.implicitly_wait(1)
            if putid is not None:    
                putid.send_keys("jeyong914@gmail.com")
                time.sleep(2)
                putpassword=driver.find_element_by_xpath("//input[@id='pass']")
                putpassword.send_keys("robot369@!")
                time.sleep(2)
                login=driver.find_element_by_xpath("//label[@class='login_form_login_button uiButton uiButtonConfirm']")
                login.click()
                time.sleep(3)

        except:
            print("logging in by page 2")

        ##login2##
        try:
            putid2=driver.find_element_by_xpath("//input[@type='text']")
            driver.implicitly_wait(1)
            if putid2 is not None:
                putid2.send_keys("jeyong914@gmail.com")
                time.sleep(2)
                putpass2=driver.find_element_by_xpath("//input[@type='password']")
                putpass2.send_keys("robot369@!")
                time.sleep(2)
                login=driver.find_element_by_xpath("//button[@class='_42ft _4jy0 _6lth _4jy6 _4jy1 selected _51sy']")
                login.click()
                time.sleep(3)

        except:
            print("logging in by page 1")


        ##search##

        findsearchbox=driver.find_element_by_xpath("//input[@class='_1frb']")
        findsearchbox.send_keys(self.keyword)
        time.sleep(1)
        searchbutton=driver.find_element_by_xpath("//button[@files-testid='facebar_search_button']")
        searchbutton.click()
        postsbutton=driver.find_element_by_xpath("//li[@class=' _5vwz _45hc']/a[@class='_3m1v _468f']")
        hrefelem=postsbutton.get_attribute('href')
        driver.get(hrefelem)
        try:
            morebutton = driver.find_element_by_xpath("//a[@class='_6ojs']")
            mbtelem=morebutton.get_attribute('href')
            driver.get(mbtelem)
            time.sleep(1)
        except:
            print("showing all posts")
        last_height = driver.execute_script("return document.documentElement.scrollHeight")
        #print(last_height)
        while(True):
            try:
                items=driver.find_elements_by_xpath("//div[@class='_19_p']")
                if (len(items)>=self.nUrl):
                    break
                driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
                time.sleep(2)
                driver.implicitly_wait(3)
                new_height = driver.execute_script("return document.documentElement.scrollHeight")
                print(last_height, "NEXT PAGE****************", new_height)
                if new_height == last_height:
                    break
                last_height=new_height
                    
                print("\n\nEND OF SCROLL****************\n\n");
            except:
                print("driver can't pick element")
        urllist = []
        urlsource = driver.find_elements_by_xpath("//span[@class='_6-cm']/a")
        for u in urlsource:
            url=u.get_attribute("href")
            urllist.append(url)
        print(*urllist,sep='\n')
        print(len(urllist))

        dtNow = datetime.now()
        dtStr = dtNow.strftime("%Y-%m-%d %H:%M:%S")

        conn = pymysql.connect(host='106.246.169.202', user='root', password='robot369',
                                       db='crawl', charset='utf8mb4')
        curs = conn.cursor()



        for Url in urllist:
            sql0 = "select * from urllist where url=\'" + Url + "\' " \
                                   + "and keyword=\'"+self.keyword+"\' "
            curs.execute(sql0)
            rows = curs.fetchall()
            if len(rows)==0:
         
          
                sql = "insert into urllist(keyword, channel, accesstime, url, crawled) " \
                              + "values (\'%s\', \'%s\', \'%s\', \'%s\', \'%s\')" % \
                              (self.keyword, self.channel, dtStr, Url, 'F')
                curs.execute(sql)
                conn.commit()

        conn.close()

        driver.close()


class FacebookCrawler:

    def __init__(self, keyword, channel):
        self.keyword = keyword
        self.channel = channel
        self.path = os.path.dirname(os.path.realpath(__file__))
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

        #popup control#
        option = Options()

        option.add_argument("--disable-infobars")
        option.add_argument("start-maximized")
        option.add_argument("--disable-extensions")

        # Pass the argument 1 to allow and 2 to block
        option.add_experimental_option("prefs", { 
            "profile.default_content_setting_values.notifications": 2 
        })

        driver = webdriver.Chrome(options=option, executable_path=self.path+"\chromedriver.exe")
        driver.get('https://www.facebook.com')

        ##login##
        try:
            putid=driver.find_element_by_xpath("//input[@id='email']")
            driver.implicitly_wait(1)
            if putid is not None:    
                putid.send_keys("jeyong914@gmail.com")
                time.sleep(2)
                putpassword=driver.find_element_by_xpath("//input[@id='pass']")
                putpassword.send_keys("robot369@!")
                time.sleep(2)
                login=driver.find_element_by_xpath("//label[@class='login_form_login_button uiButton uiButtonConfirm']")
                login.click()
                time.sleep(3)

        except:
            print("already logged in1")

        ##login2##
        try:
            putid2=driver.find_element_by_xpath("//input[@type='text']")
            driver.implicitly_wait(1)
            if putid2 is not None:
                putid2.send_keys("jeyong914@gmail.com")
                time.sleep(2)
                putpass2=driver.find_element_by_xpath("//input[@type='password']")
                putpass2.send_keys("robot369@!")
                time.sleep(2)
                login=driver.find_element_by_xpath("//button[@class='_42ft _4jy0 _6lth _4jy6 _4jy1 selected _51sy']")
                login.click()
                time.sleep(3)

        except:
            print("already logged in2")
            
        #getUrlfromDB#
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
            try:
                close_button = driver.find_element_by_xpath("//a[@class='_xlt _418x']")
                close_button.click()
            except:
                print("it is not a video")

            articletext= []
            #get article text and publishtime#
            try:
                wantedarticle = driver.find_element_by_xpath("//div[@class='_1dwg _1w_m _q7o']")
                arp1 = wantedarticle.find_element_by_xpath(".//abbr[@files-utime]")
                arp2 = arp1.get_attribute('files-utime')
                articlepubtime = datetime.fromtimestamp(int(arp2))
                articlet = wantedarticle.find_element_by_xpath(".//div[@files-testid='post_message']/div/p")
                articletext = self.cleanse(articlet.text)
                print(articlepubtime)
                print(articletext)
            except:
                print("no article found")
            #select all comments#
            comment = []
            pubtime = []
            try:
                optionbutton=driver.find_element_by_xpath("//a[@files-testid='UFI2ViewOptionsSelector/link']")
                optionbutton.click()
                selectables=driver.find_elements_by_xpath("//div[@files-testid='UFI2ViewOptionsSelector/menuOption']")
                for selectable in selectables:
                    if '최신순' or '오름차순' in selectable.text:
                        print(selectable.text)
                        selectable.click()
                        time.sleep(1)
                        break

                #select article#
                want_article = driver.find_element_by_xpath("//div[@files-testid='UFI2CommentsList/root_depth_0']")

            #click more comments#
                while True:
                    try:
                        morecommentsbt = want_article.find_element_by_xpath(".//a[@files-testid='UFI2CommentsPagerRenderer/pager_depth_0']")
                        morecommentsbt.click()
                        driver.implicitly_wait(0.1)
                        time.sleep(0.1)
                        print("clicked")
                    except:
                        print("showing all comments")
                        break

            #show reply-comments#
                while True:
                    try:
                        repcomments = want_article.find_elements_by_xpath(".//a[@files-testid='UFI2CommentsPagerRenderer/pager_depth_1']")
                        print("repcomments found")
                        time.sleep(0.1)
                        for repcomment in repcomments:
                            driver.execute_script("arguments[0].click();", repcomment)
                            time.sleep(0.1)
                            print("reply-comment clicked")
                        break
                    except:
                        print("showing all reply-comments")
                        break



            #read comments and publishtime#
               
                wantedarticle=driver.find_element_by_xpath("//div[@files-testid='UFI2CommentsList/root_depth_0']")
                try:
                    commentbox=wantedarticle.find_elements_by_xpath(".//ul[@class='_7791']/li/div")
                    for cbox in commentbox:
                        try:
                            ctexts=cbox.find_elements_by_xpath(".//div[@files-testid='UFI2Comment/body']/div/span/span[@class='_3l3x']/span")
                            for ctext in ctexts:
                                comment.append(ctext.text)
                                print(ctext.text)
                                if ctext.text is not None:
                                    ptime=cbox.find_element_by_xpath(".//ul[@files-testid='UFI2CommentActionLinks/root']/li/a/abbr")
                                    dtime=ptime.get_attribute('files-utime')
                                    a = datetime.fromtimestamp(int(dtime))
                                    pubtime.append(a)
                                    print(a)
                        except:
                                ("This comment has no text")
                except:
                    print("no comments")

            except:
                print("no comments")

            print("\n\n\n\n\n\n\n")
            print(*comment,sep='\n')
            print(*pubtime, sep = '\n')
            print(len(comment))
            print(len(pubtime))


            sql = "insert into htdocs(keyword, channel, url, accesstime, publishtime, htmltext, role)" \
                              + "values (\'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\')" % \
                              (self.keyword, self.channel, url, dtStr, articlepubtime, articletext, 'article')
            
            curs.execute(sql)
            conn.commit()
     
    
            for c, p in zip(comment,pubtime):
                cText=self.cleanse(c)
                if len(cText) !=0:
                    sql = "insert into htdocs(keyword, channel, url, accesstime, publishtime, htmltext, role)" \
                          + "values (\'%s\', \'%s\', \'%s\',\'%s\', \'%s\', \'%s\', \'%s\')" % \
                          (self.keyword, self.channel, url, dtStr, p, cText, 'comment')
                    curs.execute(sql)
            conn.commit()


             ###updatepubtime###
            try:
                sqlu = "update urllist set crawled=\'T\', crawltime=\'%s\', publishtime=\'%s\' where keyword=\'%s\' and url=\'%s\'" %(dtStr, articlepubtime, self.keyword, url)
                curs.execute(sqlu)
                conn.commit()
            except:
                continue

        conn.close()

        driver.close()    
