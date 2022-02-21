from crawLibNavercafe import CrawlLibNaverCafe

keyword= "라이즈오브킹덤즈"
crawler = CrawlLibNaverCafe(keyword=keyword)
crawler.crawl_contents_threading()