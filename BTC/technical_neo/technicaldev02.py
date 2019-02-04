#coding: utf-8
from datetime import datetime, timedelta, timezone
import MySQLdb
import sys
import numpy
import pandas as pd
import talib
import matplotlib.pyplot as plt
import statsmodels.api as sm
import technicalkit #自作ライブラリ

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
smashr = talib.SMA(npprices, timeperiod=25)
smalng = talib.SMA(npprices, timeperiod=100)
#乖離率
shrdev = technicalkit.MAdeviationrate(npprices, smashr)
lngdev = technicalkit.MAdeviationrate(npprices, smalng)
#閾値の出し方
'''
tmp1 = shrdev[25:len(shrdev) - 1]
tmp2 = lngdev[100:len(lngdev) - 1]
tmp1 = numpy.sort(tmp1)
tmp2 = numpy.sort(tmp2)
thres1under = tmp1[int(len(tmp1)*0.025)]
thres1up = tmp1[int(len(tmp1)*0.975)]
thres2under = tmp2[int(len(tmp2)*0.025)]
thres2up = tmp2[int(len(tmp2)*0.975)]
print(thres1up, thres1under, thres2up, thres2under)
'''

#売買
pointslist = []
pointslist.append(technicalkit.MAdevpoint(shrdev, -0.0037, 0.0033))
pointslist.append(technicalkit.MAdevpoint(lngdev, -0.008, 0.0063))
#print("\ntimeperiod=25", file=sys.stderr)
#print(pointslist[0], file=sys.stderr)
#print("\n\ntimeperiod=100", file=sys.stderr)
#print(pointslist[1], file=sys.stderr)
#for row in pointslist[1]:
    #if row["GC"] < row["DC"]:
        #print(row, file=sys.stderr)
        #print(npprices[row["GC"]], npprices[row["DC"]], file=sys.stderr)

#描画
shrups = []
shrunders = []
lngups = []
lngunders = []
for _ in range(len(shrdev)):
    shrups.append(0.0033)
    shrunders.append(-0.0037)
    lngups.append(0.0063)
    lngunders.append(-0.0080)

updatas_s = [npprices, smashr]
updatas_l = [npprices, smalng]
upcolors = ['black', 'red']
uplabels1 = ["raw", "SMA25"]
uplabels2 = ["raw", "SMA100"]
indicators_s = [shrdev, shrups, shrunders]
indicators_l = [lngdev, lngups, lngunders]
indicolors = ['green', 'red', 'blue']
indilabels = ["deviation rate", "sell signal", "buy signal"]
technicalkit.plot_with_indicator(rang, True, updatas_s, upcolors, uplabels1, indicators_s, indicolors, indilabels, upxlabel="Time", upylabel="Price", indixlabel="Time", indiylabel="Deviation rate", fontsize=16)
technicalkit.plot_with_indicator(rang, True, updatas_l, upcolors, uplabels2, indicators_l, indicolors, indilabels, upxlabel="Time", upylabel="Price", indixlabel="Time", indiylabel="Deviation rate", fontsize=16)
#technicalkit.plot_with_indicator(rang, True, updatas_s, upcolors, indicators_s, indicolors)
#technicalkit.plot_with_indicator(rang, True, updatas_l, upcolors, indicators_l, indicolors)

#これ本当に定常過程なのか？？？
'''
adftest_shrdev = sm.tsa.stattools.adfuller(shrdev[25:len(shrdev) - 1])
adftest_lngdev = sm.tsa.stattools.adfuller(lngdev[100:len(lngdev) - 1])
print(adftest_shrdev)
print(adftest_lngdev)
#どちらも定常過程でした


plt.hist(shrdev, bins=50, range=(-0.08, 0.08), log=False)
plt.show()
plt.hist(lngdev, bins=50, range=(-0.15, 0.15), log=False)
plt.show()
'''
#自己相関はいかに・・・
acfshr = sm.tsa.stattools.acf(shrdev[25:len(shrdev) - 1])
acflng = sm.tsa.stattools.acf(lngdev[100:len(shrdev) - 1])
print(acfshr)
print(acflng)

'''
#いいからトレードしろ
resultshr = technicalkit.MAdev_trading(pointslist[0], npprices)
resultlng = technicalkit.MAdev_trading(pointslist[1], npprices)
print("\n\nresultlng", file=sys.stderr)
#for row in resultlng:
    #print(row, file=sys.stderr)

technicalkit.analize_trading_result(resultlng)

print("\n\nresultshr", file=sys.stderr)
#c = 0
#for row in resultshr:
    #print(times[pointslist[1][c]["GC"]], times[pointslist[1][c]["DC"]], file=sys.stderr)
    #print(pointslist[1][c], file=sys.stderr)
    #print(row, file=sys.stderr)
    #c += 1

technicalkit.analize_trading_result(resultshr)
'''