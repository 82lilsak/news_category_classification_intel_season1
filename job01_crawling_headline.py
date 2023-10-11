from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import datetime

category = ['Politics', 'Economy', 'Social', 'Culture', 'World', 'IT']
# 페이지 순 정렬
url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100'

# df_titles = pd.DataFrame()
# 비어있는 데이터프레임. 생성
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"}
#userAgent 는 나는 ~~야 라고 기기? 웹브라우저 정보를 준는 느낌?

# resp = requests.get(url, headers=headers)
# # get(url) url의 리퀘스트를 리턴함.
# # print(list(resp))
# print(type(resp))
# # <class 'requests.models.Response'> 응답 객체.
# # resp 는 문자열로 주르륵 나열되어있어서 soup으로 html형식으로 변환 해줘야 한다.
# soup = BeautifulSoup(resp.text, 'html.parser') #parsing
# # print(soup)
# title_tags = soup.select('.sh_text_headline')
# print(title_tags)
# print(len(title_tags))
# print(type(title_tags[0]))
#
# titles = [] # 제목을 담을 빈 리스트 생성
# for title_tag in title_tags:
#     titles.append(re.compile('[^가-힣|a-z|A-Z]').sub(' ', title_tag.text))
#     sub(' ', title_tag.text))는 앞의 조건을 제외하고 공백으로 바꾼다.
# print(titles)
# print(len(titles))

df_titles = pd.DataFrame()
re_title = re.compile('[^가-힣|a-z|A-Z]')

for i in range(6):
    resp = requests.get('https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=10{}'.format(i),
                        headers=headers)
    # 마지막에 100~ 105 까지 반복.
    # 100 정치 , 101, 사회 등등등.. 요런식으로 카테고리 별로 받아온다.
    soup = BeautifulSoup(resp.text, 'html.parser') #parsing
    title_tags = soup.select('.sh_text_headline')
    titles = [] # 제목을 담을 빈 리스트 생성
    for title_tag in title_tags:
        titles.append(re.compile('[^가-힣|a-z|A-Z]').sub(' ', title_tag.text))
    df_section_titles = pd.DataFrame(titles, columns=['title']) # 제목들 데이터 프레임 생성
    df_section_titles['category'] = category[i]
    # 정치뉴스 제목 - 정치 이런형식으로 만들어줌.
    df_titles = pd.concat([df_titles, df_section_titles], axis='rows', ignore_index=True)

print(df_titles.head())
df_titles.info()
print(df_titles['category'].value_counts())
df_titles.to_csv('./crawling_data/naver_headline_news_{}.csv'.format(datetime.datetime.now().strftime('%Y%m%d')),
                 index=False)







