#coding: utf-8
from datetime import datetime, timedelta, timezone
import MySQLdb
import sys
import numpy
import pandas
import talib
import matplotlib.pyplot as plt
import technicalkit

s = "2018-10-31 12:00:00"
e = "2018-11-30 23:55:00"
sdate = datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
edate = datetime.strptime(e, '%Y-%m-%d %H:%M:%S')
#months = 1
host = "localhost"
dbname = "BTCJPYbitFlyer"
charset = "utf8"
user = "BTCminer"
passwd = ""
conn = MySQLdb.connect(db=dbname, host=host, charset=charset, user=user, passwd=passwd)
cur = conn.cursor()
table = "5minute"

sys.stderr.write(s)
sys.stderr.write("\n")
sys.stderr.write(e)
sys.stderr.write("\n")


#for i in range(months):
sql = "SELECT datetime,close,volume FROM 5minute WHERE datetime >= \'%s\' AND datetime <= \'%s\'" % (s, e)
cur.execute(sql)
dat = cur.fetchall()
times = []
prices = []
volumes = []
for row in dat:
    times.append(row[0])
    prices.append(row[1])
    volumes.append(row[2])
#print(times)
#print(prices)
#print(volumes)
rang = range(len(times))
npprices = numpy.array(prices, dtype='f8')
npvolumes = numpy.array(volumes, dtype='f8')
#SMA
smavsr = talib.SMA(npprices, timeperiod=5)
smashr = talib.SMA(npprices, timeperiod=25)
smamid = talib.SMA(npprices, timeperiod=75)
smalng = talib.SMA(npprices, timeperiod=100)
malist1 = [smavsr, smashr]#, smamid, smalng]
malist2 = [smavsr, smamid]
malist3 = [smashr, smamid]
malist4 = [smashr, smalng]
macolors1 = ['red', 'green']#, 'blue', 'purple']
macolors2 = ['red', 'blue']
macolors3 = ['green', 'blue']
macolors4 = ['green', 'purple']
malabel1 = ["SMA5", "SMA25"]
malabel2 = ["SMA5", "SMA75"]
malabel3 = ["SMA25", "SMA75"]
malabel4 = ["SMA25", "SMA100"]
#描画
technicalkit.plot_withMA(rang, True, npprices, malist1, macolors1, malabel1, xlabel=u"Time", ylabel=u"Price")
technicalkit.plot_withMA(rang, True, npprices, malist2, macolors2, malabel2, xlabel=u"Time", ylabel=u"Price")
technicalkit.plot_withMA(rang, True, npprices, malist3, macolors3, malabel3, xlabel=u"Time", ylabel=u"Price")
technicalkit.plot_withMA(rang, True, npprices, malist4, macolors4, malabel4, xlabel=u"Time", ylabel=u"Price")
#technicalkit.plot_withMA(rang, True, npprices, [smavsr], ['red'])
#GC,DC集

crosses = []
crosses.append(technicalkit.MAcross(smavsr, smashr))#(5,25)
crosses.append(technicalkit.MAcross(smavsr, smamid))#(5,75)
crosses.append(technicalkit.MAcross(smashr, smamid))#(25,75)
crosses.append(technicalkit.MAcross(smashr, smalng))#(25,100)
#crosses = technicalkit.MAcross(smavsr, smamid)
for i in range(len(crosses)):
    crosses[i] = technicalkit.XConverter(crosses[i])
#for c in crosses:
    #print(c)
    #print()

results = []
results.append(technicalkit.MAcross_trading(crosses[0], npprices))
results.append(technicalkit.MAcross_trading(crosses[1], npprices))
results.append(technicalkit.MAcross_trading(crosses[2], npprices))
results.append(technicalkit.MAcross_trading(crosses[3], npprices))
#result = technicalkit.MAcross_trading(crosses[0], npprices)
#print("SMA(5, 75)Cross:")

'''
for r in result:
    print(r, file=sys.stderr)

'''

for result in results:
    technicalkit.analize_trading_result(result)
    print()



#sys.stderr.write("\n")
'''
sdate = sdate + timedelta(days=1)
edate = edate + timedelta(days=1)
s = sdate.strftime("%Y-%m-%d %H:%M:%S")
e = edate.strftime("%Y-%m-%d %H:%M:%S")
sys.stderr.write(s)
sys.stderr.write("\n")
sys.stderr.write(e)
sys.stderr.write("\n")
'''

sys.stderr.write("\n")

#保存しないと操作が反映されない．
#一応ね
conn.commit()
conn.close()