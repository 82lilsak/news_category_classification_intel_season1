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
#userAgent 는 나는 ~~야 라고 정보를 준는 느낌?

# resp = requests.get(url, headers=headers)
# # get(url) url의 리퀘스트를 리턴함.
# # print(list(resp))
# print(type(resp))
# # <class 'requests.models.Response'> 응답 객체.
#
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
# print(titles)
# print(len(titles))

df_titles = pd.DataFrame()
re_title = re.compile('[^가-힣|a-z|A-Z]')

for i in range(6):
    resp = requests.get('https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=10{}'.format(i))
