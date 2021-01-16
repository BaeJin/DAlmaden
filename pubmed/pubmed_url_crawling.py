from engine.sql.almaden import Sql
import requests
from bs4 import BeautifulSoup

db = Sql(dbName="project_db",hostIP="datacast-rds.crmhaqonotna.ap-northeast-2.rds.amazonaws.com",userID='datacast',password='radioga12!',charset='utf8mb4')
rows = db.select('pubmed_paper',"paper_id, pubmed_url")
for index,row in enumerate(rows):
    try:
        pubmed_url_res = requests.get(row['pubmed_url'])
        bs4 = BeautifulSoup(pubmed_url_res.text, 'lxml')
        full_text_links_obj = bs4.find('div', {'class': 'full-text-links-list'})
        full_text_link = None

        for obj in full_text_links_obj.find_all('a'):
            if obj['href'].startswith('https://www.ncbi.nlm.nih.gov/pmc/articles/pmid/'):
                full_text_link = obj['href']
                break
            else:

                full_text_link = obj['href']
        print(index,full_text_link)

        db.insert('pubmed_paper_text',paper_id=row['paper_id'],text_url=full_text_link)

    except Exception as e:
        db.insert('pubmed_paper_text', paper_id=row['paper_id'], text_url=None)

        print(e)

# id1,test1 = 'PMC7594990','https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7594990/'
# id2,test2 = 'PMC7554505', 'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7554505/'
# id3, test3 = ''