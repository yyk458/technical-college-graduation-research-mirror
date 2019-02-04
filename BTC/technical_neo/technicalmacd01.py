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
#MACD
macdshr, signalshr, macdhistshr = talib.MACD(npprices, fastperiod=12, slowperiod=26, signalperiod=9)
macdlng, signallng, macdhistlng = talib.MACD(npprices, fastperiod=36, slowperiod=78, signalperiod=27)
malist1 = [macdshr, signalshr]
malist2 = [macdlng, signallng]
macolors = ['red', 'green']
malabels = ["MACD", "MACDsignal"]
'''
print("Time:", len(times))
print(rang)
print("raw:", len(npprices))
print(npprices)
print("MACD:", len(macdshr))
print(macdshr)
print("MACDsig:", len(signalshr))
print(signalshr)
'''
#描画
#technicalkit.plot_overlap(rang, True, [npprices], ['black'], ["raw"], xlabel="Time", ylabel="Price")
#technicalkit.plot_overlap(rang, True, malist1, macolors, ["MACD", "MACDsignal"], xlabel="Time", ylabel="MACD")
technicalkit.plot_with_indicator(rang, True, [npprices], ['black'], ["raw"], malist1, macolors, malabels, upxlabel=u"Time", upylabel=u"Price", indixlabel=u"Time", indiylabel=u"MACD")
technicalkit.plot_with_indicator(rang, True, [npprices], ['black'], ["raw"], malist2, macolors, malabels, upxlabel=u"Time", upylabel=u"Price", indixlabel=u"Time", indiylabel=u"MACD")


#クロス
crosses = []
crosses.append(technicalkit.MAcross(macdshr, signalshr))
crosses.append(technicalkit.MAcross(macdlng, signallng))
for i in range(len(crosses)):
    crosses[i] = technicalkit.XConverter(crosses[i])
resultshr = technicalkit.MAcross_trading(crosses[0], npprices)
resultlng = technicalkit.MAcross_trading(crosses[1], npprices)
#for r in resultshr:
#    print(r, file=sys.stderr)
technicalkit.analize_trading_result(resultshr)
print("\n\n", file=sys.stderr)
#for r in resultlng:
#    print(r, file=sys.stderr)
technicalkit.analize_trading_result(resultlng)





sys.stderr.write("\n")

#保存しないと操作が反映されない．
#一応ね
conn.commit()
conn.close()