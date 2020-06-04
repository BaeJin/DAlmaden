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



class InstagramLister:

    def __init__(self, nUrl, keyword, channel):
        self.nUrl = nUrl
        self.keyword = keyword
        self.channel = channel

    def getInstagramUrl(self):
        driver = webdriver.Firefox()
        driver.get("https://www.instagram.com/explore/tags/%s/"%(self.keyword))
        driver.implicitly_wait(5)
        login = driver.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/span/a[1]/button")
        login.click()
        driver.implicitly_wait(5)
        email = driver.find_element_by_xpath("/html/body/div[1]/section/main/div/article/div/div[1]/div/form/div[2]/div/label/input")
        email.send_keys("jykim@almaden.co.kr")
        driver.implicitly_wait(3)
        password = driver.find_element_by_xpath("/html/body/div[1]/section/main/div/article/div/div[1]/div/form/div[3]/div/label/input")
        password.send_keys("almaden7025!")
        driver.implicitly_wait(3)
        login = driver.find_element_by_xpath("/html/body/div[1]/section/main/div/article/div/div[1]/div/form/div[4]/button")
        login.click()
        driver.implicitly_wait(5)
        last_height = driver.execute_script("return document.documentElement.scrollHeight")
        #print(last_height)
        utfkeyword=self.keyword.encode()
        UrlList=[]
        seen = set(UrlList)
        count = 0
        while(True):
            time.sleep(3)
            print("\n\n\nNEXT PAGE**************\n\n\n");
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            driver.implicitly_wait(5)
            findu=driver.find_elements_by_css_selector("a")
            try:
                for element in findu:
                    url = element.get_attribute("href")
                    if url not in seen:
                        seen.add(url)
                        UrlList.append(url)
        ##              print(url)
            except Exception as e:
                print(e)
                print('maybe video is not readable')
            new_height = driver.execute_script("return document.documentElement.scrollHeight")
            driver.implicitly_wait(5)
            time.sleep(1)
            if new_height == last_height:
               count +=1
               print('last=new:',count)
               if count>10:
                 break
            elif new_height != last_height:
                count =0

            last_height=new_height
            UrlList = [x for x in UrlList if x.startswith('https://www.instagram.com/p/')]
            #print(*UrlList, sep = "\n")
            print(len(UrlList))
            if (len(UrlList)>=self.nUrl):
                break
            
            print(len(UrlList))
            
        print("\n\n\nEND OF SCROLL*****************\n\n\n");

        dtNow = datetime.now()
        dtStr = dtNow.strftime("%Y-%m-%d %H:%M:%S")

        conn = pymysql.connect(host='106.246.169.202', user='root', password='robot369',
                                       db='crawl', charset='utf8mb4')
        curs = conn.cursor()

        for Url in UrlList:

            sql0 = "select * from urllist where url=\'"+ Url+"\'"\
                                +"and keyword=\'"+self.keyword+"\'"
            curs.execute(sql0)
            rows = curs.fetchall()
            if len(rows)<1 :
                sql = "insert into urllist(keyword, channel, accesstime, url, crawled) " \
                              + "values (\'%s\', \'%s\', \'%s\', \'%s\', \'%s\')" % \
                              (self.keyword, self.channel, dtStr, Url, 'F')
                curs.execute(sql)
            conn.commit()

        conn.close()


class InstagramCrawler:


    def __init__(self, keyword, channel):
        self.keyword = keyword
        self.channel = channel


    def cleanse(self, text):

        text = text.replace('#',' ')
        text = re.sub('[,/$.@*\"※&%ㆍ』\\‘|\(\)\[\]\<\>`\'…》]', '', text)
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
        conn = pymysql.connect(host='106.246.169.202', user='root', password='robot369',
                                       db='crawl', charset='utf8mb4')
        curs = conn.cursor(pymysql.cursors.DictCursor)

        sql = "select * from urllist where keyword=\'%s\' and channel=\'%s\' and crawled=\'%s\'" % \
              (self.keyword, self.channel, 'F')

        print(sql)
        curs.execute(sql)

        rows = curs.fetchall()
        print("Total %s urls targeted..."%(len(rows)))

        instalist=[]
        print(rows)
        for row in rows:
            url = row['url']
            now = datetime.now()
            dtStr = now.strftime("%Y-%m-%d %H:%M:%S")
        #get url
            driver.get(url)

            driver.implicitly_wait(3)

            #+
            while True:
                try:
                    
                    click_select = driver.find_element_by_xpath("//button[@class = 'dCJp8 afkep']/span[@class='glyphsSpriteCircle_add__outline__24__grey_9 u-__7']")
                    click_select.click()

                except:
                    break
             
            print("+끝")

            #댓글더보기

            while True:
                
                try:
                    click_select2 = driver.find_element_by_xpath("//li[@class='lnrre']/button[@class ='Z4IfV sqdOP yWX7d        ']")
                    click_select2.click()
                    
                except:
                    break

            print("댓글더보기 끝")

            #답글보기

            try:
                clickables = driver.find_elements_by_xpath("//div[@class='Igw0E     IwRSH      eGOV_     ybXk5    _4EzTm']/button[@class='sqdOP yWX7d        ']")
                print(clickables)
            except:
                clickables = [ ]

            for clickable in clickables:
                print(clickable.text)
            print("\n\n=====================================\n\n")






            for clickable in clickables:
                print(clickable.text)
                if '답글 보기' in clickable.text :
                    clickable.click()
                        
                

            print("답글 보기 끝")

            

            elements=driver.find_elements_by_xpath("//div[@class='C4VMK']/span")
            pubtime = driver.find_elements_by_xpath("//time")

            datetimes=[]
            for t in pubtime:
                a=t.get_attribute('datetime')
                b=a.split('.')
                c=b[0].split('T')
                time=c[0]+' '+c[1]
                datetimes.append(time)
            print(datetimes)
            print(len(datetimes))

            pubtimeArticle = datetimes[0] if len(datetimes)>0 else None
            if len(elements) != 0:
                article = self.cleanse(elements[0].text)
                comments = []
                pubtimeComments = []
                for i, element in enumerate(elements):
                    if i>=1:
                        dt=pubtimeArticle
                        if len(datetimes)>1:
                            dt=datetimes[i]
                        print(i, element.text, dt)
                        #texts=element.text
                        comments.append(element.text)
                        pubtimeComments.append(dt)
    ##                    if len(datetimes)>1:
    ##                        for j, dt in enumerate(datetimes):
    ##                            if j>=1:
    ##                                comments[texts]=dt
    ##                    else:
    ##                        comments[texts]=datetimes[0]

                print("Article:", article, pubtimeArticle)
                print("# of comments:", len(comments))
                print(comments)
                print(pubtimeComments)

                for i, cmt in enumerate(comments):
                    pubtime = pubtimeComments[i]
                    cText = self.cleanse(cmt)
                    print(i, cText, pubtime)
                #sys.exit(1)
                
                sql = "insert into htdocs(keyword, channel, url, accesstime, publishtime, htmltext, role)" \
                              + "values (\'%s\', \'%s\', \'%s\', \'%s\', \'%s\',\'%s\', \'%s\')" % \
                              (self.keyword, self.channel, url, dtStr, pubtimeArticle, article, 'article')
            
                curs.execute(sql)
                conn.commit()

                for i, cmt in enumerate(comments):
                    pubtime = pubtimeComments[i]
                    cText = self.cleanse(cmt)
                    if len(cText) !=0:
                        sql = "insert into htdocs(keyword, channel, url, accesstime, publishtime, htmltext, role)" \
                          + "values (\'%s\', \'%s\', \'%s\',\'%s\', \'%s\', \'%s\', \'%s\')" % \
                          (self.keyword, self.channel, url, dtStr, pubtime, cText, 'comment')
                        curs.execute(sql)
                conn.commit()

                    
            ###updatepubtime###
            try:
                sqlu = "update urllist set crawled=\'T\', publishtime=\'%s\', crawltime=\'%s\' where keyword=\'%s\' and url=\'%s\'" %(pubtimeArticle, dtStr, self.keyword, url)
                curs.execute(sqlu)
                conn.commit()
            except Exception as e:
                sqlu = "delete from urllist where url='\%s\'"%(url)
                curs.execute(sqlu)
                conn.commit()
                print(e)

        conn.close()

            

             
        
        
    
    

