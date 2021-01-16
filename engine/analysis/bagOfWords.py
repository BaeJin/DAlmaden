import re
from collections import Counter
import pandas as pd

def get_gap_bows(bow1, bow2) :
    pass

def get_bow_df(seqOfTokensSeq, duplicate_count=False, relative_count = False, filter_words_channel = None) :
    '''
    :param seqOfTokensSeq: e.g. [['a','b','b'],['a','b','b,'c']]
    :return: {a:2, b:4, c:1}
    '''
    if duplicate_count :
        seq = [token for tokens in seqOfTokensSeq for token in tokens]
    else :
        seq = [token for tokens in seqOfTokensSeq for token in set(tokens)]
    bow_df = pd.DataFrame(Counter(seq).most_common())
    bow_df = bow_df.rename(columns = {0 : 'word', 1 : 'n'})

    if filter_words_channel :
        bow_df = filter_words_bow(bow_df, filter_words_channel)

    if relative_count :
        bow_df['n'] = bow_df['n'] / max(bow_df['n'])

    return bow_df


def filter_words_bow(bow_df, channel = "") :

    filterKeywords = []

    if channel == "instagram":
        extendKeywords = ["인스타그램", "인스타", "팔로우", "맞팔", "인친", "셀스타그램", "그램", "스타"]
    elif channel == "naverblog":
        extendKeywords = ["포스팅", "블로그", "댓글", "이웃추가"]
    elif channel == "twitter":
        extendKeywords = ["트윗", "RT", "트위터"]
    elif channel == "navernews":
        extendKeywords = ["없음", "헤럴드", "역필", "투데이", "머니", "코리아", "기자", "오마이", "구독", "연합", "채널", "네이버", "뉴시스",
                            "금지", "저작", "무단", "뉴스", "재배포"]
    else :
        extendKeywords = []

    filterKeywords.extend(extendKeywords)

    bow_df = bow_df[bow_df['word'].str.len()>=2]
    bow_df = bow_df[~bow_df['word'].isin(filterKeywords)]

    return bow_df

def filter_words_bow_manual(bow_df, words=[]) :
    bow_df = bow_df[~bow_df['word'].isin(words)]
    return bow_df

