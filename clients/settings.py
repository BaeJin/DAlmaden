from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://root:robot369@10.96.5.179:3306/datacast2?charset=utf8mb4",encoding='utf-8')

MAX_N_NOUN = 500
MAX_N_ADJ = 500
MAX_N_VERB = 500
N_COMB = 7

