import numpy as np
import pyodbc
import matplotlib.pyplot as plt
import matplotlib as mpl

datee = input("請輸入民國年月:")#110/01
conn = pyodbc.connect('DRIVER={SQL Server};user=sa;password=1234;database=stock;SERVER=USER-PC\ASP')
cursor = conn.cursor()
cursor.execute("SELECT * FROM 台積電")
rows = cursor.fetchall()
cursor.close()
conn.close()
ro = []
date = []
f_Volume = []
i_Volume = []
for i in range(len(rows)):
    if datee in rows[i][1] :
        ro.append(rows[i])
for row in ro:
    da = int(row.date[7:9])
    dat = row.date[0:6]
    f_Vo = int(row.foreign_investors.replace(',',''))
    i_Vo = int(row.investment_trust.replace(',',''))
    date.append(da)
    f_Volume.append(f_Vo)
    i_Volume.append(i_Vo)
max_f_Volume = str(max(f_Volume))
min_f_Volume = str(min(f_Volume))
a=np.linspace(int(max_f_Volume),int(min_f_Volume),10,dtype=int)
a=a.tolist()
Volume = []
for i in range(len(a)):
    b=str(a[i])
    vol=b.replace(b[-4:],'0000')
    vol=int(vol)
    Volume.append(vol)
min_f_Volume = int(min_f_Volume.replace(min_f_Volume[-4:],'0000'))
Volume.append(min_f_Volume)
c=dat+'月  '+row.id+'  外資買賣超日報'
g=c.replace('/','.')

f,f1,d,d1=[],[],[],[]
for i in range(len(f_Volume)):
    if f_Volume[i]>0:
        f.append(f_Volume[i])
        d.append(date[i])
    else:
        f1.append(f_Volume[i])
        d1.append(date[i])
        
mpl.rcParams['font.sans-serif'] = ['KaiTi']
mpl.rcParams['font.serif'] = ['KaiTi']
width=0.25         
x1=d                                                #X 軸 (第一組)
y1=f                                                   #Y 軸
x2=d1                                               #X 軸 (第二組)
y2=f1                                              #Y 軸
plt.bar(x1,y1,width=0.6,color="r",label='買超')                  #繪製長條圖
plt.bar(x2,y2,width=0.6,color="g",label='賣超')                  #繪製長條圖
plt.xticks([p + width/2 for p in date], date)          #設定 X 軸刻度標籤
plt.yticks(Volume, Volume)                         #設定 Y 軸刻度標籤
plt.legend()                                       #顯示圖例
plt.title(c)                                       #設定圖形標題
plt.xlabel('DATE')                                 #設定 X 軸標籤
plt.ylabel('Volume')                               #設定 Y 軸標籤
plt.savefig('{}.jpg'.format(g)) 
plt.show()


conn = pyodbc.connect('DRIVER={SQL Server};user=sa;password=1234;database=stock;SERVER=USER-PC\ASP')
cursor = conn.cursor()
cursor.execute("SELECT * FROM 台積電")
rows = cursor.fetchall()
cursor.close()
conn.close()
ro = []
date = []
financing_Volume = []
for i in range(len(rows)):
    if datee in rows[i][1]:
        ro.append(rows[i])
for row in ro:
    da = int(row.date[7:9])
    dat = row.date[0:6]
    date.append(da)
    financing_Volume.append(int(row.financing_balance))
max_financing_Volume = str(max(financing_Volume))
min_financing_Volume = str(min(financing_Volume))
m_financing_Volume = int((int(max_financing_Volume)+int(min_financing_Volume))/(len(financing_Volume)-15))
a=np.linspace(int(max_financing_Volume),int(min_financing_Volume),10,dtype=int)
Volume=a.tolist()
Volume.append(int(min_financing_Volume))
c=dat+'月  '+row.id+'  融資餘額日報'
g=c.replace('/','.')

f,f1,d,d1=[],[],[],[]
for i in range(len(financing_Volume)):
    if int(financing_Volume[i])>0:
        f.append(financing_Volume[i])
        d.append(date[i])
    else:
        f1.append(financing_Volume[i])
        d1.append(date[i])
        
mpl.rcParams['font.sans-serif'] = ['KaiTi']
mpl.rcParams['font.serif'] = ['KaiTi']
width=0.25         
x1=d                                                #X 軸 (第一組)
y1=f                                                   #Y 軸
x2=d1                                               #X 軸 (第二組)
y2=f1                                              #Y 軸
plt.bar(x1,y1,width=0.6,color="r",label='增加')                  #繪製長條圖
plt.bar(x2,y2,width=0.6,color="g",label='減少')                  #繪製長條圖
plt.xticks([p + width/2 for p in date], date)          #設定 X 軸刻度標籤
plt.yticks(Volume, Volume)                         #設定 Y 軸刻度標籤
plt.legend()                                       #顯示圖例
plt.title(c)                                       #設定圖形標題
plt.xlabel('DATE')                                 #設定 X 軸標籤
plt.ylabel('Volume')                               #設定 Y 軸標籤
plt.savefig('{}.jpg'.format(g)) 
plt.show()


