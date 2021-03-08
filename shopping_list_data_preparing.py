import pandas as pd  
import numpy as np  
import sys
from pandas import DataFrame
import re

df= pd.read_excel('naver_shopping_list.xlsx', engine='openpyxl')

def 상품목록전처리(df):
        #네이버랭킹 순위
        df['네이버랭킹'] = df['Unnamed: 0'] + 1
        #가격
        df['가격'] = df['price'].replace('무료', '0', regex=True).replace(r"\D", "", regex=True).replace(np.NaN, 0).astype(np.int16)
        #배송비
        df['배송비'] = df['del_charge'].replace('무료', '0', regex=True).replace(r"\D", "", regex=True).replace(np.NaN, 0).astype(np.int16)

        #몰등급 
        df['몰등급'] = df['mall_grade'].replace('굿서비스', 'None', regex=True).map(네이버쇼핑몰등급)

        #조리양
            #알고리즘 : 상품명에서 추출한 조리양 정보를 우선으로 하고, 상품명에 없는 경우 상세 정보에 있는 조리양 정보로 대체한다. 
            # 2~3인분은 2.5로 변환

            #1. 상품명 정보에서 인분 정보 추출하기
        df['제목조리양'] = df['title'].str.extract(r'([\d]|[\d].[\d])*인').replace(np.NaN, 0)
        df['제목조리양'] = df['제목조리양'].map(조리양얻기).astype(np.float)

            #2. 상세정보에서 인분 정보 추출하기
        df['상세조리양'] = df['detail'].str.extract(r'([\d])인').astype(float)

            #3.조리양 컬럼에 제목조리양 값 있으면 제목조리양, 제목조리양이 0일 때 상세조리양 값을 넣는다
            # 람다함수 활용
        df['조리양'] = df.apply( lambda series : series["제목조리양"] != 0 and series["제목조리양"] or series["상세조리양"]  , axis=1) 

        #구매건수, 찜하기, 리뷰
        df['구매건수'] = df['keep'].str.extract(r"구매건수([\d\,]+)").replace(r"\D", "", regex=True).replace(np.NaN, 0).astype(np.int16)
        df['찜하기'] = df['keep'].str.extract(r"찜하기([\d\,]+)").replace(r"\D", "", regex=True).replace(np.NaN, 0).astype(np.int16)
        df['리뷰'] = df['keep'].str.extract(r"리뷰([\d\,]+)").replace(r"\D", "", regex=True).replace(np.NaN, 0).astype(np.int16)
        
        #상품명
        df['상품명']=df['title'].replace(r"쿠킹\w+", "", regex=True)
        df['상품명']=df['상품명'].replace(r"밀키\w+", "", regex=True)
        df['상품명']=df['상품명'].replace(r'\([^)]*\)', "", regex=True)
        df['상품명']=df['상품명'].replace(r"\W", "", regex=True)




def 네이버쇼핑몰등급(x):
    if x =='None':
        return 1
    elif x == '파워':
        return 2
    elif x == '빅파워':
        return 3
    elif x == '프리미엄':
        return 4

def 조리양얻기(text):
    text_sub = re.sub(r'~|-|\,', '/', str(text))
    if "/" in text_sub:
        portions = text_sub.split('/')
        avg = ( int(portions[0]) +  int(portions[1])) / 2
        return avg
    else:
        return text

상품목록전처리(df)

df = df.rename(index=str, columns={"category": "분류", "mall": '판매자'})
df[['네이버랭킹','상품명','가격','분류','조리양','찜하기','구매건수','리뷰','판매자','몰등급','배송비']].to_excel('naver_shopping_list_cleaned.xlsx')