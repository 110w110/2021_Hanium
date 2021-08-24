import time
import datetime
import urllib.request
import urllib.parse
import math
from selenium import webdriver
# 크롬드라이버 연결

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable_logging"])
driver = webdriver.Chrome(options=options)
data_list = []


def crawl(pro,cur):

    product = pro[1]
    plusUrl = urllib.parse.quote_plus(product)
    url = f'https://www.lotteon.com/search/search/search.ecn?render=search&platform=pc&q={plusUrl}&mallId=1'
    driver.get(url)
    
    try:
        a = driver.find_element_by_css_selector('.srchResultNull.srchNullCharacter1')
        print("해당 상품 없음")
        return
        #driver.quit()
        #sys.exit()
    except Exception:
        driver.find_element_by_css_selector('.srchProductUnitImageArea').click()
        time.sleep(1)

    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(1)

    # 상품명, 가격 확인 
    product = driver.find_element_by_css_selector('.productName').text 
    print("상품명:",product) 
    try: # 리뷰 없을때
        nodata = driver.find_element_by_css_selector(".dataNull.default")
        print(nodata.text)
        return
        #driver.quit()
        #sys.exit()
    except Exception: # 리뷰 있을때
        review_total = driver.find_element_by_css_selector('.reviewCount').text 
        review_total = review_total.replace("건","")
        print("리뷰 개수:",review_total)

    sql = "INSERT IGNORE INTO product (lotte) VALUES (%s)"
    cur.executemany(sql, review_total)