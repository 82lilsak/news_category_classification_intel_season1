from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import pandas as pd
import re
import time
import datetime




options = ChromeOptions()
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
options.add_argument('user-agent=' + user_agent)
options.add_argument("lang=ko_KR")
# options.add_argument('headless')  # 브라우저를 보여주지 않음.
# options.add_argument('window-size=1920x1080')
# options.add_argument("disable-gpu")
# options.add_argument("--no-sandbox")

# 크롬 드라이버 최신 버전 설정
service = ChromeService(executable_path=ChromeDriverManager().install())

# chrome driver
driver = webdriver.Chrome(service=service, options=options)  # <- options로 변경
# driver.get(url)

# //*[@id="section_body"]/ul[1]/li[3]/dl/dt[2]/a    // idx가 1부터 시작함.
# xpath는 중복 요소가 없다. 서로 다른 유니크한 xpath를 갖고 있어야 한다.
category = ['Politics', 'Economy', 'Social', 'Culture', 'World', 'IT']
pages = [110, 110, 110, 75, 110, 72]
df_titles = pd.DataFrame() # for 문에 들어가기 전에 비어있는 데이터 프레임 생성.

# 카테고리 별로 비슷한 숫자로 맞춰주는 것이 좋다.  너무 작은것을 기준으로 하면 안됨.
# 데이터를 약간 손해 보기는 한다.

for l in range(6):
    section_url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=10{}'.format(l)
    titles = []
    for k in range(1, pages[l] + 1):  # pages[l] + 1 // pages[0]+1 // 110 이 들어가야 111을 가져옴.
        url = section_url + '#&date=%2000:00:00&page={}'.format(k)
        driver.get(url)
        time.sleep(0.5)
        # 페이지 로드에 시간이 걸리기때문에 time.slppe(s) 를 넣어줘야 한다. 시간을 마냥 늘리면 포문이 반복이 많아서 시간이 오래 걸리게 된다.
        for i in range(1, 5):
            for j in range(1, 6):
                title = driver.find_element('xpath',
                                            '//*[@id="section_body"]/ul[{}]/li[{}]/dl/dt[2]/a'.format(i, j)).text
                title = re.compile('[^가-힣]').sub(' ', title)  # 가~ 힣 까지만 남기고 나머지는 ' ' 공백으로 변경/.
                titles.append(title)
    df_section_title = pd.DataFrame(titles, columns=['titles'])
    # 1섹션이 끝날때마다 섹션 타이틀을 만든다.
    df_section_title['category'] = category[l]
    df_titles = pd.concat([df_titles, df_section_title], ignore_index=True)
df_titles.to_csv('./crawling_data/crawling_data.csv', index=False)


print(df_titles.head())
df_titles.info()
print(df_titles['category'].value_counts())
