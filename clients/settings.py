from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://root:almaden7025!@61.98.230.194:3306/datacast2?charset=utf8mb4",encoding='utf-8')

MAX_N_NOUN = 500
MAX_N_ADJ = 500
MAX_N_VERB = 500
N_COMB = 7

