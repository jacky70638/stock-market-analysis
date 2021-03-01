import requests,time
from bs4 import BeautifulSoup
import pyodbc

param = {"":""}
date = input("請輸入買賣日期:")#20210201
stockNo = input("請輸入股票代號:")
param[0] = date
header={#模擬瀏覽器的東西,模擬自己變成網站、偽裝網站
        "Cookie": "JSESSIONID=281957DD0B4492234CD8D3D3B18A0BFC; _ga=GA1.3.426055122.1600497576; _gid=GA1.3.773701738.1600497576; _gat=1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
        }

conn = pyodbc.connect('DRIVER={SQL Server};user=sa;password=1234;database=stock;SERVER=USER-PC\ASP')
cursor = conn.cursor()

da=[]
for i in range(1,32):
    if len(str(i)) == 1:
        i = '0'+str(i)
        i = str(date[0:6])+i
        url = "https://www.twse.com.tw/fund/T86?response=html&date={}&selectType=24".format(i)
        da.append(url)   
    else:
        i = str(date[0:6])+str(i)
        url = "https://www.twse.com.tw/fund/T86?response=html&date={}&selectType=24".format(i)
        da.append(url) 
        
financing=[]
for i in range(1,32):
    if len(str(i)) == 1:
        i = '0'+str(i)
        i = str(date[0:6])+i
        url = "https://www.twse.com.tw/exchangeReport/MI_MARGN?response=html&date={}&selectType=24".format(i)
        financing.append(url)
    else:
        i = str(date[0:6])+str(i)
        url = "https://www.twse.com.tw/exchangeReport/MI_MARGN?response=html&date={}&selectType=24".format(i)
        financing.append(url) 
        
for i in range(0,31):
    url = da[i]
    try:
        data = requests.get(url,params=param,headers=header).text
        con = BeautifulSoup(data,"html.parser")
        items = con.find("table")
        tr = items.find_all("tr")
        stock_No = 0
        content = 0
        for row in tr:
            stock_No += 1
            td = row.text.split()
            if stock_No == 1:
                date = td[0]
                b=date[0]+date[1]+date[2]+'/'+date[4]+date[5]+'/'+date[7]+date[8]
            if td[0] == stockNo:
                foreign_investors = td[4]
                investment_trust = td[10]
                print(date,foreign_investors,investment_trust)
        cursor.execute("""UPDATE 台積電 SET foreign_investors='{}',investment_trust='{}'
                        WHERE date='{}'""".format(foreign_investors,investment_trust,b))#更新資料  
        print(da[i])
        print()
        time.sleep(10)
    except:
        pass

for i in range(0,31):
    url = financing[i]
    try:
        data = requests.get(url,params=param,headers=header).text
        con = BeautifulSoup(data,"html.parser")
        items = con.find("table")
        tr = items.find_all("tr")
        stock_No = 0
        content = 0
        for row in tr:
            stock_No += 1
            td = row.text.split()
            if stock_No == 1:
                date = td[0]
                b=date[0]+date[1]+date[2]+'/'+date[4]+date[5]+'/'+date[7]+date[8]
            if td[0] == stockNo:
                financing_balance = int(td[6].replace(',',''))-int(td[5].replace(',',''))
                print(date,financing_balance)
        cursor.execute("""UPDATE 台積電 SET financing_balance='{}'
                        WHERE date='{}'""".format(financing_balance,b))#更新資料
        print(financing[i])
        print()
        time.sleep(10)
    except:
        pass

conn.commit()
cursor.close()
conn.close()
       
        
        
        
        
        
        
        