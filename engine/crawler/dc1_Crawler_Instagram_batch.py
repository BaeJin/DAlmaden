from pathlib import Path
import sys
sys.path.append('../')
sys.path.append(Path.cwd().parents[0])
print(sys.path)
from engine.crawler.crawlLibInstagram_o import CrawlLibInstagram

username = 'jykim@almaden.co.kr'
password = 'almaden7025!'
keyword = sys.argv[1]
num_content = int(sys.argv[2])

crawler = CrawlLibInstagram(username,password,keyword,num_content)
crawler.crawinstagram()
