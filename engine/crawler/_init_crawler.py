from engine.crawler.crawlLibnaverblog import CrawlLibnaverBlog
from engine.crawler.crawlLibnavercafe import CrawlLibnaverCafe
from engine.crawler.crawlLibnavernews import CrawlLibnaverNews
from engine.crawler.crawlLibInstagram import CrawlLibInstagram
from engine.crawler.crawlLibnavershopping import CrawlLibNavershopping
from engine.crawler.crawlLibyoutube import CrawlLibYoutube


def crawl_contents(task_id=None,
                   channel=None,
                   keyword=None,
                   from_date=None,
                   to_date=None,
                   n_crawl=None,
                   n_total=None):

    if channel == 'naverblog':
        print(f"{task_id},naverblog crawling start")
        crawler_obj = CrawlLibnaverBlog(task_id=task_id, keyword=keyword, from_date=from_date, to_date=to_date,
                                        n_crawl=n_crawl, n_total=n_total)
        crawler_obj.crawl()
        del crawler_obj

    if channel == 'navercafe':
        print(f"{task_id},navercafe crawling start")
        print(n_crawl,n_total)
        crawler_obj = CrawlLibnaverCafe(task_id=task_id, keyword=keyword, from_date=from_date, to_date=to_date,
                                        n_crawl=n_crawl, n_total=n_total)
        crawler_obj.crawl()
        del crawler_obj

    if channel == 'navernews':
        print(f"{task_id},navernews crawling start")
        crawler_obj = CrawlLibnaverNews(task_id=task_id, keyword=keyword, from_date=from_date, to_date=to_date,
                                        n_crawl=n_crawl, n_total=n_total)
        crawler_obj.crawl()
        del crawler_obj

    if channel == 'instagram':
        print(f"{task_id},instagram crawling start")
        crawler_obj = CrawlLibInstagram(task_id=task_id, keyword=keyword, from_date=None, to_date=None,
                                        n_crawl=n_crawl, n_total=n_total, need_reply=False)
        crawler_obj.start_requests()
        del crawler_obj

def crawl_review(contents_id=None,
                 task_id=None,
                   keyword=None,
                   n_total=None,
                 prod_desc=None,channel=None):
    if channel == 'navershopping':
        crawler_obj = CrawlLibNavershopping(contents_id=contents_id,task_id=task_id, keyword=keyword, n_total=n_total,prod_desc=prod_desc)
        crawler_obj.crawl()

    if channel == 'youtube':
        crawler_obj = CrawlLibYoutube(contents_id=contents_id,task_id=task_id, keyword=keyword, n_total=n_total,prod_desc=prod_desc)
        crawler_obj.crawl()


