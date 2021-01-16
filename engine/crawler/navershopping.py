from almaden import SeleniumDriver
from almaden import Sql
import re
from crawler_utils import cleanse
def crawl(keyword, productURL, productName, comment="navershopping") :
    #db명
    db = Sql('dalmaden')
    task_id = db.insert('task_log',comment=comment)
    driver = SeleniumDriver()

    driver.get(productURL)

    #직접 스크롤 다운해서 리뷰 페이지 표출
    input("직접 스크롤 다운해서 리뷰 페이지 표출")
    #아래 코드 실행
    maxPage = 10
    num=0
    while True :
        #getcontents
        #리뷰 컨테이너
        ele = driver.driver.find_element_by_css_selector("#area_review_list .detail_list_review")
        ele.text
        #리뷰 리스트
        ele = ele.find_elements_by_css_selector('li')
        for e in ele:

            print("################################")
            try :
                num+=1
                print(e.text)
                channel = 'navershopping'
                text_info = e.find_elements_by_css_selector('div.area_status_user span')
                author,date_raw,option = "","",""
                try :
                    author = text_info[0].text
                    date_raw = '20'+text_info[1].text
                    date_lst = date_raw.split(".")
                    post_date = "-".join(date_lst[:-1])
                    option = e.find_element_by_css_selector('p.text_option').text
                except :
                    pass
                text = e.find_element_by_css_selector('span.text').text
                text = cleanse(text)
                rating = e.find_element_by_css_selector('span.number_grade').text
                db.insert('crawled_data',
                          task_id = task_id,
                          channel = channel,
                          keyword = keyword,
                          num = num,
                          post_date=post_date,
                          title = productName,
                          text=text,
                          author=author,
                          url = productURL,
                          etc1=rating,
                          etc2 = option
                          )
            except Exception as ex :
                print(ex)

        #pagenation
        #현재 페이지
        pageNum = int(driver.driver.find_element_by_css_selector("nav._review_list_page a[aria-selected='true']").text)
        print(pageNum)
        nextPage = pageNum+1
        if nextPage > maxPage :
            #다음페이지목록
            driver.driver.find_element_by_xpath(
                "//*[contains(@class,'module_pagination')]//a[contains(@class,'next')]").click()
            maxPage = pageNum+10
        else :
            #다음페이지
            driver.driver.find_element_by_xpath(
                "//*[contains(@class,'module_pagination')]//*[text()=%d]"%(nextPage)).click()

def cleanse(text) :
    #DB 저장을 위한 최소한의 클린징
    text = re.sub(u"[^\x20-\x7E가-힣]"," ",text)
    text = re.sub(u"\\s+", " ", text)
    return text.strip()