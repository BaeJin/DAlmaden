rows = ['주식추천좀 해주세요 씨말 인생 좆되기 일보직전이네','정글러는 다른 포지션의 의견을 무시해야 티어를 올릴 수 있다.hts ','hts 뉴스 전체기사를 보면 댓글이 웃기고 재밋다']
filter_word_list = ['추천','증권사','댓글']
includ_any_word_list = ['수수료', '브랜드', '평판', '편리', '신뢰', '투표', '친절', '개설', 'hts', 'HTS', '어플', '앱', '혜택', '이벤트', '우대',
                        '금리', '계좌', '모바일', '서비스']

rows = list(filter(lambda row:
                   (not any(filter_word in row for filter_word in filter_word_list)) and
                   any(includ_any_word in row for includ_any_word in includ_any_word_list),
                   rows)
            )
print(rows)