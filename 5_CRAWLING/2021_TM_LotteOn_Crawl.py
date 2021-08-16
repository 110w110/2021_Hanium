import time
import datetime
import urllib.request
import urllib.parse
import math
from selenium import webdriver
import pandas as pd
import sys

#크롬드라이버 연결
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable_logging"])
driver = webdriver.Chrome(options=options)
data_list = []

product = "아이스 브레이커스 민트"
plusUrl = urllib.parse.quote_plus(product)
url = f'https://www.lotteon.com/search/search/search.ecn?render=search&platform=pc&q={plusUrl}&mallId=1'
driver.get(url)

try:
    a = driver.find_element_by_css_selector('.srchResultNull.srchNullCharacter1')
    print("해당 상품 없음")
    driver.quit()
    sys.exit()
except Exception:
    driver.find_element_by_css_selector('.srchProductUnitImageArea').click()
    time.sleep(1)

driver.switch_to.window(driver.window_handles[-1])
time.sleep(1)

# 상품명, 가격 확인 
product = driver.find_element_by_css_selector('.productName').text 
print("상품명:",product) 
price = driver.find_element_by_css_selector('.price').text
price = price.replace("\n원","")
price = price.replace(",", "")
print("가격:",price)

def get_page_data(): 
    users = driver.find_elements_by_css_selector('.userName') # 사용자명 수집 
    ratings = driver.find_elements_by_css_selector('.staring') # 평점 수집 
    reviews = driver.find_elements_by_css_selector('.texting') #리뷰 수집
    dates = driver.find_elements_by_css_selector('.date') #날짜 수집
    hours = "시간 전"
    
    if len(users) == len(reviews):
        for i in range(len(users)):
            user = users[i].text
            rating = ratings[i+2].text
            rating = rating.replace("평점","")
            rating = int(rating)
            review = reviews[i].text
            review = review.replace("\n"," ")
            date = dates[i].text
            date = date.replace(".","")
            if hours in date:
                date = str(datetime.date.today())
                date = date.replace("-", "")
            data = (user, int(rating), review, int(date))
            data_list.append(data)
            print(data)

try: # 리뷰 없을때
    nodata = driver.find_element_by_css_selector(".dataNull.default")
    print(nodata.text)
    driver.quit()
    sys.exit()
except Exception: # 리뷰 있을때
    review_total = driver.find_element_by_css_selector('.reviewCount').text 
    review_total = review_total.replace("건","")
    review_grade = driver.find_element_by_css_selector('.staring').text
    review_grade = review_grade.replace("평점\n","")
    print("평점:", review_grade) 
    print("리뷰 개수:",review_total)

#페이지별 리뷰 개수
review_per_page = 5
review_total = review_total.replace(",","")
total_page = int(review_total) / review_per_page 
total_page = math.ceil(total_page) 
print("리뷰 페이지 수:", total_page)    


print("수집 시작") # 첫 페이지 수집하고 시작 
get_page_data()
for page in range(0, total_page-1):
        print(str(page+1)+"page 수집 끝")
        driver.find_element_by_css_selector('.next').click() 
        time.sleep(1)
        get_page_data()
print(str(page) + " page 수집 끝") 
print("수집 종료") 
print(data_list)

df = pd.DataFrame(data_list) 
print(df) 
