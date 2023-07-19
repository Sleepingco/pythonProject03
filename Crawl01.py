import urllib.request
from bs4 import BeautifulSoup
import pymysql

try:
  conn = pymysql.connect(host='127.0.0.1', user='root', password='himedia',
                         db='drill', charset='utf8', autocommit=True)
  if conn is None:
    print('MySQL Drill DB 연결실패')
    exit(0)
  cur = conn.cursor()
  # cur.execute('delete from stock')
except Exception as e:
  print('error:', e)

arPage = [43, 34]
for sosok in range(2):  # KOSPI
  try:
    for x in range(1, arPage[sosok] + 1):
      url = f'https://finance.naver.com/sise/sise_market_sum.naver?&page={x}'
      src_code = urllib.request.urlopen(url)

      plain_text = src_code.read().decode('euc-kr')

      convert_data = BeautifulSoup(plain_text, 'html.parser')
      for start in [2, 10, 18, 26, 34, 42, 50, 58, 66, 74]:
        for i in range(start, start + 5):
          selector1 = f'#contentarea > div.box_type_l > table.type_2 > tbody > tr:nth-child({i}) > td:nth-child(2) > a'
          # contentarea > div.box_type_l > table.type_2 > tbody > tr:nth-child(2) > td:nth-child(2) > a
          stock = convert_data.select_one(selector1)

          code = stock['href'][-6:]
          name = stock.string
          print(type(name))
          # print(stock)  # [<a class="tltle" href="/item/main.naver?code=005930">삼성전자</a>]

          print(code, name, end='')  # 종목명
          selector1 = f'#contentarea > div.box_type_l > table.type_2 > tbody > tr:nth-child({i}) > td:nth-child(3)'
          price = convert_data.select_one(selector1)
          price = price.string.replace(',', '')
          print(f'{price:9s}', end='')  # 현재가
          selector1 = f'#contentarea > div.box_type_l > table.type_2 > tbody > tr:nth-child({i}) > td:nth-child(7)'
          amount = convert_data.select_one(selector1)
          amount = amount.string.replace(',', '')
          print(f'{amount:20s}')  # 시가총액
          # sql = f"replace into stock values ({sosok},'{code}','{name}',{price},{amount})"
          # cur.execute(sql)
  except Exception as e:
    print('error:', e)
  print('-'*30)
print('Crawling Bot was terminated')
# 2~6
# 10~14
# 18~22
# 26~30
# 34~38
# 42~46
# 50~54
# 58~62
# 66~70
# 74~78
# for atag in convert_data.find_all('a'):
#   print(atag.string)
# 개발자도구 - > Elements -> Copy Selector
# selector1 = f'#contentarea > div.box_type_l > table.type_2 > tbody > tr:nth-child(3) > td:nth-child(2) > a'
# stock = convert_data.select(selector1)
# print(stock)
