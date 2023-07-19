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
  url = f'https://finance.naver.com/marketindex/?tabSel=exchange#tab_section'
  src_code = urllib.request.urlopen(url)
  plain_text = src_code.read().decode('euc-kr')
  convert_data = BeautifulSoup(plain_text, 'html.parser')
  for i in range(59):
    selector1 = f'body > div > table > tbody > tr:nth-child({i}) > td.tit > a'
    xrate = convert_data.select_one(selector1)
    name = xrate.string
    print(type(name))
    print(name, end='')  # 종목명
    selector1 = f'body > div > table > tbody > tr:nth-child({i}) > td.sale'
    standard = convert_data.select_one(selector1)
    print(f'{standard:10.2f}', end='')  # 현재가
    selector1 = f'body > div > table > tbody > tr:nth-child({i}) > td:nth-child(7)'
    conv = convert_data.select_one(selector1)
    conv = conv.string.replace(',', '')
    print(f'{conv:5.3f}')  # 시가총액
    sql = f"replace into stock values ('{name}',{standard},{conv})"
    cur.execute(sql)
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
