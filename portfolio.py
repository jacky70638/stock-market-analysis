import requests,pyodbc
from bs4 import BeautifulSoup
# import K線圖
param = {"":""}
date = input("請輸入日期:")#20210201
stockNo = input("請輸入股票代號:")
param[0] = date
param[1] = stockNo
header={#模擬瀏覽器的東西,模擬自己變成網站、偽裝網站
        "Cookie": "JSESSIONID=281957DD0B4492234CD8D3D3B18A0BFC; _ga=GA1.3.426055122.1600497576; _gid=GA1.3.773701738.1600497576; _gat=1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
        }
url = "https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=html&date={}&stockNo={}".format(date,stockNo)
data = requests.get(url,params=param,headers=header).text
con = BeautifulSoup(data,"html.parser")
items = con.find("table")
tr = items.find_all("tr")

stock_No,content,a = 0,0,0
foreign_investors,investment_trust,financing_balance = 0,0,0
conn = pyodbc.connect('DRIVER={SQL Server};user=sa;password=1234;database=stock;SERVER=USER-PC\ASP')
cursor = conn.cursor()
for row in tr:
    stock_No += 1
    if stock_No == 1:
        tdd = row.text.split()
        title = tdd[0]+"\t"+tdd[1]+"\t"+tdd[2]

    content += 1
    if content > 2:
        td = row.text.split()
        datee=td[0]
        start_time=td[3].replace(",","")
        high=td[4].replace(",","")
        low=td[5].replace(",","")
        end_time=td[6].replace(",","")
        price_dif=td[7].replace(",","")
        Volume=td[8].replace(",","")
        con = datee,start_time,high,low,end_time,price_dif,Volume

        cursor.execute("SELECT date FROM 台積電")
        rows = cursor.fetchall()
        a=[]
        for row in rows:
            a.append(row)
        b = len(a)
        c=0
        for i in range(0,b):
            if datee in a[i]:
                c+=1
                break
        if c==0:
            cursor.execute("insert into 台積電(id,date,start_time,high,low,end_time,price_dif,Volume,foreign_investors,investment_trust,financing_balance) values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(tdd[2],datee,start_time,high,low,end_time,price_dif,Volume,foreign_investors,investment_trust,financing_balance))
conn.commit()
cursor.close()
conn.close()


















