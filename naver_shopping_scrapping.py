from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from pandas import DataFrame
import pandas as pd
from tqdm import notebook

#원하는 상품 목록 결과 페이지 접근
driver = webdriver.Chrome(r'./chromedriver')
url = "https://search.shopping.naver.com/search/category?catId=50006808&frm=NVSHTTL&origQuery&pagingIndex=1&pagingSize=40&productSet=window&query&sort=rel&timestamp=&viewType=list"
#테스트 페이지
#url = "https://search.shopping.naver.com/search/category?catId=50006808&delivery=2&frm=NVSHPRC&maxPrice=20000&minPrice=0&origQuery&pagingIndex=1&pagingSize=40&productSet=window&query&sort=rel&timestamp=&viewType=list"

driver.get(url)

#푸드윈도 상품만 선택 클릭
sel = '#lb_window_fresh'
ui = driver.find_element_by_css_selector(sel)
ui.click()

data_list =[]
#한 화면에 있는 목록 40개 반복하기
def 상품목록얻기(num):
    try:
        for j in notebook.tqdm(range(1, num)):
            for i in range(1, 41):

            #상품명 얻기
                sel = f"ul > div > div:nth-child({i}) > li > div > div.basicList_info_area__17Xyo > div.basicList_title__3P9Q7 > a" 
                ui = driver.find_element_by_css_selector(sel)
                title = ui.text 

            #가격 얻기
                sel = f"#__next > div > div.style_container__1YjHN > div > div.style_content_wrap__1PzEo > div.style_content__2T20F > ul > div > div:nth-child({i}) > li > div > div.basicList_info_area__17Xyo > div.basicList_price_area__1UXXR"
                ui = driver.find_element_by_css_selector(sel)
                price = ui.text 
            
            #카테고리
                sel= f"#__next > div > div.style_container__1YjHN > div > div.style_content_wrap__1PzEo > div.style_content__2T20F > ul > div > div:nth-child({i}) > li > div > div.basicList_info_area__17Xyo > div.basicList_depth__2QIie > a:nth-child(4)"
                ui = driver.find_element_by_css_selector(sel)
                category = ui.text

            #디테일 정보 얻기(카테고리, 테마, 조리양, 조리시간, 조리난이도)
                try:
                    sel = f"#__next > div > div.style_container__1YjHN > div > div.style_content_wrap__1PzEo > div.style_content__2T20F > ul > div > div:nth-child({i}) > li > div > div.basicList_info_area__17Xyo > div.basicList_desc__2-tko > div.basicList_detail_box__3ta3h"
                    ui = driver.find_element_by_css_selector(sel)
                    detail = ui.text
                except:
                    detail = "None"
             
             #판매 지수 정보 얻기 (리뷰, 구매건수, 등록일, 찜하기) 
                sel = f"#__next > div > div.style_container__1YjHN > div > div.style_content_wrap__1PzEo > div.style_content__2T20F > ul > div > div:nth-child({i}) > li > div > div.basicList_info_area__17Xyo > div.basicList_etc_box__1Jzg6"
               
                ui = driver.find_element_by_css_selector(sel)
                keep = ui.text 

            #판매자명 얻기
                sel = f"#__next > div > div.style_container__1YjHN > div > div.style_content_wrap__1PzEo > div.style_content__2T20F > ul > div > div:nth-child({i}) > li > div > div.basicList_mall_area__lIA7R > div.basicList_mall_title__3MWFY > a.basicList_mall__sbVax"
                ui = driver.find_element_by_css_selector(sel)
                mall = ui.text 
             
             #몰등급 얻기
                try:
                    sel = f"#__next > div > div.style_container__1YjHN > div.style_inner__18zZX > div.style_content_wrap__1PzEo > div.style_content__2T20F > ul > div > div:nth-child({i}) > li > div > div.basicList_mall_area__lIA7R > div.basicList_mall_grade__31CEX > span"
                    ui = driver.find_element_by_css_selector(sel)
                    mall_grade = ui.text             
                except:
                    mall_grade = 'None' 

             #배송비 얻기
                try:
                    sel = f"#__next > div > div.style_container__1YjHN > div > div.style_content_wrap__1PzEo > div.style_content__2T20F > ul > div > div:nth-child({i}) > li > div > div.basicList_mall_area__lIA7R > ul > li:nth-child(2) > em"
                    ui = driver.find_element_by_css_selector(sel)
                    del_charge = ui.text             
                except:
                    del_charge = 'None'
                       


            #화면 스크롤 하기    
                driver.execute_script(f"window.scrollTo(0, {700 * i})")
 
            #딕셔너리에 정보 추가하기
                data = {} 
                data['title'] = title 
                data['price'] = price
                data['category'] = category
                data['detail'] = detail
                data['keep'] = keep
                data['mall'] = mall
                data['mall_grade'] = mall_grade
                data['del_charge'] = del_charge
                print(j, i, data)
                data_list.append(data) 


            #다음 페이지 버튼 클릭
            sel = 'a.pagination_next__1ITTf'
            ui = driver.find_element_by_css_selector(sel)
            ui.click()
            time.sleep(5)
    except:
        print('error')
    
상품목록얻기(21)    
    
#dataframe만들고 excel로 내보내기
df = DataFrame(data_list)
df.to_excel("naver_shopping_list.xlsx")
