import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import pymysql
import re


class NaverNewsLister:
    def __init__(self,s_page ,maxpage, keyword, channel, stdate, endate):
        self.maxpage = maxpage
        self.keyword = keyword
        self.channel = channel
        self.stdate = stdate.replace("-",".")
        self.endate = endate.replace("-",".")
        print(self.stdate, self.endate)
        self.s_page = s_page
        # crawler(self.maxpage, self.query, self.s_date, self.e_date)


    def crawl(self, keywor):
        keyword=self.keyword
        stdate = self.stdate
        endate = self.endate
        s_from = stdate.replace(".", "")
        e_to = endate.replace(".", "")
        maxpage = self.maxpage
        s_page = self.s_page
        maxpage_t = (int(maxpage)-1)*10+1   #1page =1 , 2page=11, 3page=21 ...

        while s_page < maxpage_t:
            #print(page)

            url = f"https://search.naver.com/search.naver?where=news&query={keyword}&sort=0&ds={stdate}&de={endate}&nso=so%3Ar%2Cp%3Afrom"+s_from+"to"+e_to+"%2Ca%3A&start="+str(s_page)
            req = requests.get(url)
            cont = req.content
            soup = BeautifulSoup(cont,'html.parser')
            check = soup.select("._sp_each_url")
            #print(check)

            for urls in soup.select("._sp_each_url"):
                if urls["href"].startswith("https://news.naver.com"):  # naver news 홈 에 존재하는 뉴스
                    news_detail_dict = self.get_news(urls["href"])

                    try:
                        conn = pymysql.connect(host='106.246.169.202', user='root', password='robot369',
                                               db='crawl2', charset='utf8mb4')
#             192.168.0.105
                        curs = conn.cursor()

                        #url 으로 중복 검사하기
                        sql0 = "select * from htdocs where url=\'" + news_detail_dict['url'] + "\' " \
                               + "and keyword=\'"+self.keyword+"\'"
                        curs.execute(sql0)
                        rows = curs.fetchall()
                        if len(rows)==0:
                            sql = "insert into naver_news(keyword, stdate, endate, publishtime, title, reporter, email, pcompany, channel, url, htmltext, img)"\
                            + "values (\'%s\', \'%s\', \'%s\', \'%s\', \'%s\',\'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\')" % \
                            (self.keyword, self.stdate, self.endate, news_detail_dict['pdate'], news_detail_dict['title'], news_detail_dict['reporter'], news_detail_dict['email'],
                             news_detail_dict['pcompany'], self.channel, news_detail_dict['url'], news_detail_dict['content'], news_detail_dict['img'])
                            curs.execute(sql)
                            conn.commit()
                            print('crawling success:',news_detail_dict['url'])
                        else:
                            print('DB에'+news_detail_dict['url']+'가 존재합니다.')
                    except Exception as e:
                        print(e)
            s_page +=10

    def get_news(self, url):
        news_detail_dict = {}
        try:
            breq = requests.get(url)
            bsoup = BeautifulSoup(breq.content, 'html.parser')

            title = bsoup.select('h3#articleTitle')[0].text # 대괄호는 h3 # articleTitle 인 것 중 첫번째 그룹만 가져오겠다.
            title = self.get_title(title)

            publishtime = bsoup.select('.t11')[0].get_text()[:11] #publishtime 가져오기

            _text = bsoup.select('#articleBodyContents')[0].get_text().replace('\n', " ")   #본문
            btext = _text.replace("// flash 오류를 우회하기 위한 함수 추가 function _flash_removeCallback() {}", "")

            text = self.get_text(btext)

            pcompany = bsoup.select('#footer address')[0].a.get_text() if bsoup.select('#footer address')[0].a is not None else None

            img_src = self.get_image(bsoup, url)
            rp = self.get_name(btext, url)
            email = self.get_email(btext, url)

            news_detail_dict = {'keyword': self.keyword, 'title': title,'reporter': rp, 'email': email, 'pcompany': pcompany,'pdate': publishtime,  'content': text, 'url': url,
                                 'img': img_src}
        except Exception as e:
            print('cannot crawling this page:'+url)
            return news_detail_dict

        return news_detail_dict

    def get_name(self,btext, url):           #text 에서 기자 이름 추출하기
        try :
            pharse = re.findall(r"[\w']+", btext)  # 특수문자 공백 단위로 문장 쪼개기
            for i, keyword in enumerate(pharse):  # 기자를 포함하는 문장을 모두 rp 에 담아준다. 기자 를 포함하는 문장중 마지막 문장이 기자 이름을 포함하기 때문에 덮어씌어준다.
                if keyword == '기자':
                    index = i
            rp = pharse[index - 1]
        except Exception as ex:
            print('failed to extract name:'+url)
            return 'None'
        return rp

    def get_email(self, btext, url):     #text 에서 기자 email 추출하기
        try :
            # 기자 email 뽑아내기
            email = re.findall('\S+@\S+', btext)
            email = email[0]
            email = re.sub('[가-힣]', "", email)
            email = re.sub('\'', '', email)
            email = re.sub('\"', '', email)
            email = re.sub('\[.*\)', "", email)
            email = re.sub('[ㄱ-ㅎㅏ-ㅣ]+', "", email)
            email = re.sub('\-|\]|\{|\}|\(|\)*', "", email)
        except Exception as ex:
            print('failed to extract email:'+url)
            return 'None'
        return email

    def get_image(self, bsoup, url):
        try:
            img = bsoup.select('#articleBodyContents')[0]
            img = img.find_all("img")  # img 태그 찾기
            img_src_list = []
            for i in img:
                img_src = i['src']  # img 태그 중 src 속성 저장
                if 'http' in img_src:  # http로 소스 읽어들일 수 있는 이미지만 저장한다.
                    img_src_list.append(img_src)  # img 다운로드를 위해 list 에 추가한다.
            text = re.sub('\'', '', str(img_src_list))
            text = re.sub('\"', '', text)
            text = re.sub('\[', "", text)
            text = re.sub('\]', "", text)
        except Exception as ex:
            print('failed to extract image:' + url)
            return 'None'
        return text

    def cleansing(self,text):

        text = re.sub('[,#/:$@*\"※&%ㆍ』\\‘|\(\)\[\]\<\>`\'…》]', '', text)

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
        text = re.sub('\\-|\]|\{|\}|\(|\)', "", text)

        text = re.sub(u'[\u2702-\u27b0]', '', text)
        text = re.sub(u'[\uD800-\uDFFF]', '', text)
        text = re.sub(u'[\U0001F600-\U0001F64F]', '', text)  # emoticons
        text = re.sub(u'[\U0001F300-\U0001F5FF]', '', text)  # symbols & pictographs
        text = re.sub(u'[\U0001F680-\U0001F6FF]', '', text)  # transport & map symbols
        text = re.sub(u'[\U0001F1E0-\U0001F1FF]', '', text)  # flags (iOS)
        return text

    def get_title(self, title):

        title = self.cleansing(title)
        return title

    def get_text(self, btext):

        text = self.cleansing(btext)
        return text
        # text = re.sub(u'[\U0001F600-\U0001F1FF]', '', text)

