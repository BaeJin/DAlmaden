from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException
from threading import Thread
import sys
import re
from datetime import datetime
from calcDate import dateCalculator
import time
import requests, bs4, pymysql


class YouTubeCrawler:
    def __init__(self, name, channel):
        self.MAX_VIDEOS = 20
        self.MAX_COMMENTS = 30
        self.name=name
        self.dateCalc=dateCalculator()
        self.channel = channel

    def openBrowser(self):
        options = Options()
        options.headless = False
        self.driver = webdriver.Firefox(options=options)

    def closeBrowser(self):
        self.driver.quit()

    def cleanse(self, text):
        # enclosed chars 
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

        

    def getVideoItems(self, keyword, nUrl, startDate, endDate):
        self.keyword = keyword
        self.MAX_VIDEOS = nUrl
        self.startDate = startDate
        self.endDate = endDate
        
        #driver = webdriver.Firefox()
        self.driver.get("https://www.youtube.com/results?search_query=%s"%(self.keyword))
        self.driver.implicitly_wait(30)
        last_height = self.driver.execute_script("return document.documentElement.scrollHeight")
        #print(last_height)
        while(True):
            items=self.driver.find_elements_by_xpath("//ytd-video-renderer[@class='style-scope ytd-item-section-renderer']")
            if (len(items)>=self.MAX_VIDEOS):
                break
            self.driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            time.sleep(2)
            self.driver.implicitly_wait(30)
            new_height = self.driver.execute_script("return document.documentElement.scrollHeight")
            print(self.name,last_height, "NEXT PAGE****************", new_height, ", # of videos = %d"%(len(items)))
            if new_height == last_height:
                break
            last_height=new_height
            
        print(self.name, "\n\nEND OF SCROLL****************\n\n");

        dtNow = datetime.now()
        dtStr = dtNow.strftime("%Y-%m-%d %H:%M:%S")

        items=self.driver.find_elements_by_xpath("//ytd-video-renderer[@class='style-scope ytd-item-section-renderer']")
        #items=self.driver.find_elements_by_xpath("//a[@id='video-title']")
        videoList=[]
        conn = pymysql.connect(host='106.246.169.202', user='root', password='robot369',
                                       db='crawl', charset='utf8mb4')
        # conn = pymysql.connect(host='103.55.190.32', user='wordcloud', password='word6244!@',
        #                        db='crawl', charset='utf8mb4')
        curs = conn.cursor()
        
        for item in items:
            try:
                videoLink=item.find_element_by_xpath(".//a[@id='video-title']")
                title=videoLink.text
                title=self.cleanse(title)
                url=videoLink.get_attribute('href')
                label=videoLink.get_attribute('aria-label')
                author = item.find_element_by_xpath("//*[@id='text']/a").text
                author=self.cleanse(author)
    ####최초 공개일: 비디오#####
                metas = item.find_elements_by_xpath(".//div[@id='metadata-line']/span")
                views=metas[0].text
                views = re.sub(u"조회수 ", "", views)
                try:
                    if '최초 공개일' in metas[0].text:
                        pubTime = self.dateCalc.calcDatetime(dtNow, metas[0].text)
                    else:
                        pubTime = self.dateCalc.calcDatetime(dtNow, metas[1].text)
                except:
                    continue
                #print(dtNow, metas[1].text, pubTime)
                
                duration = item.find_element_by_xpath(".//ytd-thumbnail-overlay-time-status-renderer/span").text

                print(self.name, title, url, author, views, pubTime, duration)
                print('\n')

                sql = "insert into urllist(keyword, channel, stdate, endate, accesstime, url, title, publishtime, crawled) " \
                      + "values (\'%s\', \'%s\', \'%s\', \'%s\', \'%s\',\'%s\',\'%s\' ,\'%s\', \'%s\')" % \
                      (self.keyword, self.channel, self.startDate, self.endDate, dtStr, url, title, pubTime, 'F')
                curs.execute(sql)
                conn.commit()


                videoList.append(YouTubeVideoListInfo(title, url, pubTime, dtStr))
            except:
                continue
        #driver.quit()
        conn.close()

        return videoList

    def readUrlListFromDB(self, keyword):
        conn = pymysql.connect(host='106.246.169.202', user='root', password='robot369',
                               db='crawl', charset='utf8mb4')
        # 192.168.0.105
        # conn = pymysql.connect(host='103.55.190.32', user='wordcloud', password='word6244!@',
        #                        db='crawl', charset='utf8mb4')
        curs = conn.cursor(pymysql.cursors.DictCursor)
        sql = "select * from urllist where keyword=\'%s\' and channel=\'%s\' and crawled=\'%s\'" % \
              (keyword, self.channel, 'F')

        print(sql)
        curs.execute(sql)

        rows = curs.fetchall()
        print("Total %s urls targeted..."%(len(rows)))

        videoList=[]
        
        for row in rows:
            url = row['url']
            title = row['title']
            pubTime = row['publishtime']
            accTime = row['accesstime']

            videoList.append(YouTubeVideoListInfo(title, url, pubTime, accTime))

        conn.close()

        return videoList


    def getContent(self, videoItem):
        try:
            dtNow = datetime.now()
            dtStr = dtNow.strftime("%Y-%m-%d %H:%M:%S")

            url = videoItem.url
            print("\n"+self.name, "opening "+url)
            self.driver.get(url)
            self.driver.implicitly_wait(30)
            time.sleep(3)

            title = self.driver.find_element_by_xpath("//h1[@class='title style-scope ytd-video-primary-info-renderer']").text
            title=self.cleanse(title)
            print(self.name, "<Title> ", title[0:30])

            replyCount=-1
            
            try:
                replyCountSection = self.driver.find_element_by_xpath("//h2[@id='count']/yt-formatted-string[@class='count-text style-scope ytd-comments-header-renderer']")
                replyCountTxt=replyCountSection.text
                replyCountTxt = re.sub(u'댓글 ', '', replyCountTxt)
                replyCountTxt = re.sub(u'개', '', replyCountTxt)
                replyCountTxt = re.sub(u',', '', replyCountTxt)
                replyCount=int(replyCountTxt)
            except:
                replyCount=0

            print(self.name, "  reply = ",replyCount)

            try:
                moreBtn = self.driver.find_element_by_xpath("//yt-formatted-string[@class='more-button style-scope ytd-video-secondary-info-renderer']")
                if moreBtn.is_displayed():
                    moreBtn.click()
            except:
                pass
                
            time.sleep(1)
            self.driver.implicitly_wait(20)

            titleDesc = self.driver.find_element_by_xpath("//yt-formatted-string[@class='content style-scope ytd-video-secondary-info-renderer']").text
            titleDesc=re.sub('\r', ' ', titleDesc)
            titleDesc=re.sub('\n', '', titleDesc)
            titleDesc=self.cleanse(titleDesc)
            print(self.name, "<Description> ",titleDesc[0:30])

            videoContent = YouTubeVideoContentInfo(url, title, titleDesc, replyCount, videoItem.publishTime, dtStr)

            if replyCount>0:
                last_height = self.driver.execute_script("return document.documentElement.scrollHeight")
                #print(last_height)
                while(True):
                    commentThreads=self.driver.find_elements_by_xpath("//ytd-comment-thread-renderer[@class='style-scope ytd-item-section-renderer']")
                    if len(commentThreads)>=self.MAX_COMMENTS or len(commentThreads)>=replyCount :
                        break

                    self.driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
                    time.sleep(2)
                    self.driver.implicitly_wait(30)
                    new_height = self.driver.execute_script("return document.documentElement.scrollHeight")


                    playerStatus = self.driver.execute_script("return document.getElementById('movie_player').getPlayerState()")
                    print(self.name, last_height, "NEXT PAGE****************", new_height, ", # of comments = %d"%(len(commentThreads)), ", player = ", playerStatus)
                    if playerStatus == 1:
                        self.driver.execute_script("document.getElementById('movie_player').click()")
                    if new_height == last_height:
                        break
                    last_height=new_height
                    
                commentThreads=self.driver.find_elements_by_xpath("//ytd-comment-thread-renderer[@class='style-scope ytd-item-section-renderer']")
                print(self.name, "# of comments = %d"%(len(commentThreads)))

                comments=[]

                for ct in commentThreads:
                    pubDTStr = ct.find_element_by_xpath(".//yt-formatted-string[@class='published-time-text above-comment style-scope ytd-comment-renderer']/a").text
                    pubDT = self.dateCalc.calcDatetime(dtNow, pubDTStr)
                    
                    comment = ct.find_element_by_xpath(".//yt-formatted-string[@id='content-text']").text
                    comment=re.sub('\r', ' ', comment)
                    comment=re.sub('\n', '', comment)
                    comment=self.cleanse(comment)
                    print(self.name, pubDT, comment[0:20])
                    comments.append(YouTubeCommentInfo(comment, pubDT))

                videoContent.comments=comments
            else:
                videoContent.comments=[]

            return videoContent
            
            
        except NoSuchElementException as ex:
            print(self.name, 'YouTubeCrawler Error: ', ex)
            return None

    def storeContentsIntoList(self, videoInfoList, resultList):
        for vItem in videoInfoList:
            contentForItem = self.getContent(vItem)
            if contentForItem is not None:
                resultList.append(contentForItem)

    def writeDocsToDB(self, keyword, channel, contentList):
        conn = pymysql.connect(host='106.246.169.202', user='root', password='robot369',
                                       db='crawl', charset='utf8mb4')
        curs = conn.cursor(pymysql.cursors.DictCursor)

        dtNow = datetime.now()
        dtStr = dtNow.strftime("%Y-%m-%d %H:%M:%S")
        for item in contentList:
            sql = "insert into htdocs(keyword, channel, url, accesstime, publishtime, htmltext, role)" \
                  + "values (\'%s\', \'%s\', \'%s\',\'%s\', \'%s\', \'%s\', \'%s\')" % \
                  (keyword, channel, item.url, item.accessTime, item.publishTime, item.title, 'title')
            #print(sql)
            curs.execute(sql)
            conn.commit()

            sql = "insert into htdocs(keyword, channel, url, accesstime, publishtime, htmltext, role)" \
                  + "values (\'%s\', \'%s\', \'%s\',\'%s\', \'%s\', \'%s\', \'%s\')" % \
                  (keyword, channel, item.url, item.accessTime, item.publishTime, item.titleDesc, 'titleDesc')
            #print(sql)
            curs.execute(sql)
            conn.commit()

            for c in item.comments:
                cText = self.cleanse(c.text)
                sql = "insert into htdocs(keyword, channel, url, accesstime, publishtime, htmltext, role)" \
                      + "values (\'%s\', \'%s\', \'%s\',\'%s\', \'%s\', \'%s\', \'%s\')" % \
                      (keyword, channel, item.url, item.accessTime, c.publishTime, cText, 'comment')
                #print(sql)
                curs.execute(sql)
                conn.commit()

            sql = "update urllist set crawled=\'T\' where keyword=\'%s\' and url=\'%s\'" %(keyword, item.url)
            #print(sql)
            curs.execute(sql)
            conn.commit()
                
            
        conn.close()
        
class YouTubeVideoListInfo:
    def __init__(self, title, url, publishTime, accessTime):
        self.title=title
        self.url=url
        self.publishTime=publishTime
        self.accessTime=accessTime
        

class YouTubeVideoContentInfo:
    def __init__(self, url, title, titleDesc, nReply, publishTime, accessTime):
        self.url=url
        self.title=title
        self.titleDesc=titleDesc
        self.nReply=nReply
        self.comments=[]
        self.publishTime=publishTime
        self.accessTime=accessTime

class YouTubeCommentInfo:
    def __init__(self, text, pubTime):
        self.text=text
        self.publishTime=pubTime




########################################################################################################################

                                ##      ##        ##        ######    ##      ##
                                ####  ####      ##  ##        ##      ##      ##
                                ##  ##  ##    ##      ##      ##      ####    ##
                                ##  ##  ##    ##      ##      ##      ##  ##  ##
                                ##      ##    ##########      ##      ##    ####
                                ##      ##    ##      ##      ##      ##      ##
                                ##      ##    ##      ##    ######    ##      ##

########################################################################################################################

##
##
##yt = YouTubeCrawler('T0   ')
##ytVideoInfoList = yt.getVideoItems('파라오의 무덤 Part 2 피라미드 만드는 방법 | B')
##yt.driver.quit()
##
##
##
##nThread=4
##urlLists = []
##ytContentList = []
##ytCrawlers = []
##for i in range(0, nThread):
##    urlLists.append([])
##    ytContentList.append([])
##    ytCrawlers.append(YouTubeCrawler('T%d   '%(i)))
##
##
##
##idx=0
##for v in ytVideoInfoList:
##    urlListNo=idx%nThread
##    urlLists[urlListNo].append(v)
##    idx+=1
##    
##
##for i in range(0, nThread):
##    print("\n\n< In List %d>"%(i))
##    for u in urlLists[i]:
##        print(u.title[0:20])
##    
##
##th=[]
##for i in range(0, nThread):
##    th.append(Thread(target=ytCrawlers[i].storeContentsIntoList, args=(urlLists[i], ytContentList[i])))
##
##for i in range(0, nThread):    
##    th[i].start()
##
##for i in range(0, nThread):
##    th[i].join()
##
##
##for i in range(0, nThread):
##    print ("\n\n========================================================================================================\n\nAt List ",i)
##    for ycItem in ytContentList[i]:
##        print("\n\n<",ycItem.title[0:30],"> : nReply=", ycItem.nReply)
##        print(ycItem.titleDesc[0:30])
##        for c in ycItem.comments:
##            print(">>", c.pubTime, c.text[0:30]) 
##                         
##
##    
##for i in range(0, nThread):
##    ytCrawlers[i].driver.quit()
##



