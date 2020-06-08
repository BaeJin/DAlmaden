from almaden import Sql
import kss
import pandas as pd
from .cleanser import cleanse_text, cleanse_text_sentence

class Data :
    def __init__(self, dbName='dalmaden'):
        self.db = Sql(dbName)
        self.df = pd.DataFrame()

    def _load_(self, channel, keyword, fromDate, toDate, tablename='cdata'):
        where_str = f"keyword='{keyword}' and channel='{channel}' and post_date between '{fromDate}' and '{toDate}'"
        ldf = self.db.select(tablename,  "*", where_str, asDataFrame=True)
        return ldf

    def addData(self, channel, keyword, fromDate, toDate,
                tablename='cdata', unique = True, drop_by=['keyword','url']):
        nrows0 = self.df.shape[0]
        ldf = self._load_(channel, keyword, fromDate, toDate, tablename)
        print(ldf)
        nrowsldf = ldf.shape[0]

        self.df = self.df.append(ldf)
        addednRows = nrowsldf
        droppednRows = 0

        if unique:
            self.drop_duplicates(subset=drop_by)
            addednRows = self.df.shape[0]-nrows0
            droppednRows = nrowsldf - addednRows
        print(f'addData : added {addednRows} rows (dropped {droppednRows} rows)')

    def drop_duplicates(self,subset=None):
        self.df = self.df.drop_duplicates(subset=subset)

    def shape(self):
        return self.df.shape


    def getdfd(self, *colnames):
        return self.df.loc[:,list(colnames)]

    def getdfs(self, *colnames, textColName = 'text'):
        dfd = self.getdfd(*colnames)
        df_sentences = pd.DataFrame()
        nrows = dfd.shape[0]
        for i in range(nrows) :
            if i%100 == 0 :
                print(f"loader : Getting Sentences {i}/{nrows}")
            row = dfd.iloc[i]
            text = row[textColName]
            if len(text) > 0 :
                text = cleanse_text(text)
                sentences = kss.split_sentences(text)    #텍스트 길이 300 넘는게 허다하게 나옴... 체크 필요함
                for s in sentences :
                    s = cleanse_text_sentence(s)
                    if len(s) > 0 :
                        row_temp = row.copy()
                        row_temp[textColName] = s
                        df_sentences = df_sentences.append(row_temp)
            else :
                continue
        print(f"loader : Getting Sentences Done {nrows} to {df_sentences.shape[0]}")
        return df_sentences



data = Data('dalmaden')
data.addData('naverblog','복숭아','2020-03-20','2020-05-15',unique=True,drop_by=['keyword','url'])
dfd = data.getdfd('text')
dfs = data.getdfs('text')

text = "복숭아 꽃의 꿈복숭아나 살구꽃이 만발한 나무 아래를 거닐면복숭아밭에서 예쁜 복숭아 하나를 얻어 품속에 넣는 꿈잘 익은 복숭아를 얻은 꿈은복숭아나무 가지에서 잘 익은 복숭아를 따는 꿈 복숭아꿈 더보기오늘의운세내일의운세쥐띠 운세소띠 운세호랑이띠 운세토끼띠 운세용띠 운세뱀띠 운세말띠 운세양띠 운세원숭이띠 운세닭띠 운세개띠 운세돼지띠 운세부모님꿈구렁꿈쌀꿈청룡꿈무너지는꿈하이힐꿈대만꿈호통꿈주어꿈임산부꿈검은돌꿈음식꿈줄거리꿈통과꿈고이게꿈적진꿈가시꿈홀딱쇼꿈잠바꿈스트립꿈인삼꽃꿈산천꿈모란꽃꿈석고꿈종류꿈가족꿈선사꿈미역국꿈개간지꿈대나무꿈에메랄드꿈불꿈바나나꿈신발꿈줄다리기꿈학위모꿈굴뚝꿈신체꿈전화꿈화단꿈작은새꿈놀이동산꿈적군꿈식탁꿈구멍꿈찧는꿈온몸꿈산신령꿈예수꿈뜻밖꿈오이꿈위장꿈새끼꿈항구꿈검정꿈변꿈복숭아꿈빼앗는꿈틀니꿈소방차꿈"
text = "그래서 보여드릴께여!제가 색조화장을 많이 좋아하지는 않지만 기본으로 색조화장으로 깔끔해진 딥클렌징을 보여드릴께여. 다른아무것도 안하고 바로 샤워메이트 비누와 함께해본 딥클렌징!WOW!깔끔하지여!퇴근하고 돌아오면 항상 손이 지저분해져 있는 신랑도 23번 손을 씻다보면 건조하다고 하는데 샤워메이트 클렌징비누를 사용하고서는 촉촉하다고 저한테 이야기를 하더라구여. 역시 제품을 바꾸어놓으면 바로 느끼는건 바로 신랑인것 같아여. 헤헤 그리고 아침에 순하게 세안비누를 찾고 계신다면 보습과 수분 그리고 영양까지 전해주는 샤워메이트 비누와 함께 해보세여. 은은한과일향으로 하루가 상쾌하게 시작하실수있으실거예요!!"

