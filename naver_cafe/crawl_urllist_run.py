from crawLibNavercafe import CrawlLibNaverCafe

keyword= "삼국지전략판"
crawler = CrawlLibNaverCafe(keyword=keyword)

crawler.crawl_urllist()