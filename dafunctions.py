import os

import engine.crawler as crawler
from engine.preprocess.loader import Loader
from engine.analysis.bagOfWords import get_bow_df, filter_words_bow
from engine.analysis.tokenizer import get_nouns_list
from engine.analysis.kano import visualize_df_kano, get_df_kano
import tables as tables

def get_df(channel, keyword, fromDate, toDate, with_text_sentence = False) :
    table = tables.Table_htdocsRegular()
    loader = Loader(table)
    loader.addData(channel, keyword, fromDate, toDate, drop_duplicate=True)
    if with_text_sentence :
        loader.mutate_sentence()
    return loader.df

def get_df_bow(text_seq, channel, type = 'noun', duplicate_count = False) :
    if type == 'noun' :
        df = get_nouns_list(text_seq)
    else :
        pass #TBD
    df_bow = get_bow_df(df, duplicate_count)
    df_bow = filter_words_bow(df_bow, channel=channel)
    return df_bow


def get_kano(df_bowpn, filename) :
    path = os.getcwd() + "\\files\\" + filename
    df_kano = get_df_kano(df_bowpn) # label, nPos, nNeg 컬럼 있어야 함
    visualize_df_kano(df_kano, path)


def write_csv(df, filename) :
    path = os.getcwd()+"\\files\\"+filename
    df.to_csv(path)


def run_crawl(channel, keyword, startDate, endDate, nCrawl, comment=""):
    if channel == 'naverblog' :
        crawler.naverblog.crawl(keyword, startDate, endDate, nCrawl, comment)
    elif channel == 'navernews' :
        crawler.navernews.crawl(keyword, startDate, endDate, nCrawl, comment)
    elif channel == 'bigkinds' :
        crawler.bigkinds.crawl(keyword, startDate, endDate, nCrawl, comment)
    else :
        print("channel name error :",channel)