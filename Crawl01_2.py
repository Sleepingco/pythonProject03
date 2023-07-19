import urllib.request
from bs4 import BeautifulSoup
import pymysql

try:
    conn = pymysql.connect(host='127.0.0.1', user='root', password='himedia', db='drill',
                           charset='utf8',autocommit=True)
    if conn is None:
        print('MySQL Drill DB 연결실패')
        exit(0)
    cur = conn.cursor()
    # cur.execute('delete from stock')
except Exception as e:
    print('Error : ',e)

arPage=[43,34]
for sosok in range(2):
    try:
        for x in range(1,arPage[sosok]+1): # KOSPI
            url = f'https://finance.naver.com/sise/sise_market_sum.naver?&sosok={sosok}&page={x}'
            src_code = urllib.request.urlopen(url)

            plain_text = src_code.read().decode('euc-kr')

            convert_data = BeautifulSoup(plain_text, 'html.parser')
            # 개발자도구 -> Elements -> Copy Selector
            for start in [2,10,18,26,34,42,50,58,66,74]:
                for i in range(start,start+5):
                    selector1 = f'#contentarea > div.box_type_l > table.type_2 > tbody > tr:nth-child({i}) > td:nth-child(2) > a'
                    stock=convert_data.select_one(selector1) # 태그에 속성과 값을 가져옴
                    code=stock['href'][-6:] # 종목코드 추출
                    name = stock.string
                    print(code,name,end='') # 종목코드,종목명
                    selector1 = f'#contentarea > div.box_type_l > table.type_2 > tbody > tr:nth-child({i}) > td:nth-child(3)'
                    price=convert_data.select_one(selector1)
                    price=price.string.replace(',','')
                    print(f'{price:9s}',end='') # 현재가
                    selector1 = f'#contentarea > div.box_type_l > table.type_2 > tbody > tr:nth-child({i}) > td:nth-child(7)'
                    amount = convert_data.select_one(selector1)
                    amount = amount.string.replace(',','')
                    print(f'{amount:20s}') # 시가총액
                    # alter table stock change name name varchar(64) not null;
                    sql = f"replace into stock values ({sosok},'{code}','{name}',{price},{amount})"
                    cur.execute(sql)
    except Exception as e:
        print('Error : ', e)
    print('-'*30)
print('Crawling Robot was terminated.')