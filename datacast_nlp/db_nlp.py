from collections import Counter
from eunjeon import Mecab
from .almaden_sql import Sql
from kss import split_sentences
import re
from tqdm import tqdm
import random
from datetime import datetime
def run_nlp(i):
    print(i+'_process_start')
    from_db = Sql('dalmaden','1.221.75.76',3306,'root','robot369')
    db = Sql('datacast','1.221.75.76',3306,'root','robot369')

    targets = db.select('crawl_contents','contents_id, url')
    already_targets_raw = db.select('crawl_corpus','contents_id')
    already_targets = [already_target_raw['contents_id'] for already_target_raw in already_targets_raw]
    targets = [target for target in targets if target['contents_id'] not in already_targets]
    random.shuffle(targets)
    tagger = Mecab()
    tagger_id = 1
    for target in tqdm(targets) :
        print(i+'_start')
        contents_id = target['contents_id']
        url = target['url']
        contents = from_db.select('cdata','text, author','url="%s"'%(url))[0]
        text = contents['text']
        author = contents['author']
        corpus_ids = db.check_duplication('crawl_corpus',contents_id = contents_id)
        if len(corpus_ids) == 0 :
            try :
                corpus_id = db.insert('crawl_corpus',
                                      text = text,
                                      author = author,
                                      contents_id = contents_id)
            except :
                text = re.sub("[^가-힣A-z0-9\.\?\!]+", " ", text)
                corpus_id = db.insert('crawl_corpus',
                                      text=text,
                                      author=author,
                                      contents_id=contents_id)
            try :
                sentences = split_sentences(text)
            except :
                try :
                    text_refine = re.sub("[^가-힣A-z0-9\.\?\!]+"," ",text)
                    sentences = split_sentences(text_refine)
                except Exception as ex:
                    print(ex)
                    text_refine = re.sub("[^가-힣A-z0-9\.\?\!]+", " ", text)
                    sentences = [text_refine]
            if len(sentences)<0:continue
            for sentence in sentences :
                sentence_id = db.insert('analysis_sentence',
                          corpus_id = corpus_id,
                          sentence=sentence)
                sentence_refine = re.sub("[^가-힣A-z0-9\.\?\!]+", " ", sentence)
                tokens = [word+"|"+pos for word,pos in tagger.pos(phrase=sentence_refine) if pos[0] in ['N','V','M']]
                if len(tokens) > 0 :
                    counter_token = Counter(tokens)
                    for token, frequency in dict(counter_token).items() :
                        word, pos = token.split("|")
                        word_ids = db.check_duplication('analysis_word', word=word, pos=pos, tagger_id = tagger_id)
                        if len(word_ids)==0 :
                            word_id = db.insert('analysis_word', word=word, pos=pos, tagger_id = tagger_id)
                        else :
                            word_id = word_ids[0]
                        # sentence_word_ids = db.check_duplication('analysis_sentence_word', word_id=word, sentence_id = sentence_id)
                        # if len(sentence_word_ids) == 0 :
                        db.insert('analysis_sentence_word',
                                  sentence_id = sentence_id,
                                  word_id = word_id,
                                  frequency = frequency)