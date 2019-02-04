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

s = "2018-10-01 12:00:00"
e = "2018-10-31 23:55:00"
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
#smavsr = talib.SMA(npprices, timeperiod=5)
smashr = talib.SMA(npprices, timeperiod=25)
smalng = talib.SMA(npprices, timeperiod=100)
#vsrdev = technicalkit.MAdeviationrate(npprices, smavsr)
shrdev = technicalkit.MAdeviationrate(npprices, smashr)
lngdev = technicalkit.MAdeviationrate(npprices, smalng)
print(shrdev)
#描画
#updatas_s = [npprices, smashr]
#updatas_l = [npprices, smalng]
#upcolors = ['black', 'red']
#technicalkit.plot_with_indicator(rang, True, updatas, upcolors, [shrdev], ['green'])

#hist
plt.rcParams["font.size"] = 18
plt.hist(shrdev, bins=50, range=(-0.02, 0.02), log=True)
plt.show()
plt.hist(lngdev, bins=50, range=(-0.07, 0.07), log=True)
plt.show()

#恐怖の単位根検定
#adftest_shrdev = sm.tsa.stattools.adfuller(shrdev[25:len(shrdev) - 1])
#adftest_lngdev = sm.tsa.stattools.adfuller(lngdev[100:len(lngdev) - 1])
#print(adftest_shrdev)
#print(adftest_lngdev)
#print(len(shrdev[25:len(shrdev) - 1]))
#technicalkit.plotrawdata(rang, True, shrdev[25:len(shrdev) - 1])

#乖離率分布は対数正規分布(対数表示で正規分布)っぽいので，正負5%(計10%)を採用
#正負2.5%でもええんやない？
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

shrups = []
shrunders = []
lngups = []
lngunders = []
for _ in range(len(shrdev)):
    shrups.append(0.0033)
    shrunders.append(-0.0037)
    lngups.append(0.0063)
    lngunders.append(-0.0080)

'''

#再描画
'''
updatas_s = [npprices, smashr]
updatas_l = [npprices, smalng]
upcolors = ['black', 'red']
uplabels1 = ["raw", "SMA25"]
uplabels2 = ["raw", "SMA100"]
indicators_s = [shrdev, shrups, shrunders]
indicators_l = [lngdev, lngups, lngunders]
indicolors = ['green', 'red', 'red']
indilabels = ["deviation rate", "sell signal", "buy signal"]
technicalkit.plot_with_indicator(rang, True, updatas_s, upcolors, uplabels1, indicators_s, indicolors, indilabels, upxlabel="Time", upylabel="Price", indixlabel="Time", indiylabel="Deviation rate")
technicalkit.plot_with_indicator(rang, True, updatas_l, upcolors, uplabels2, indicators_l, indicolors, indilabels, upxlabel="Time", upylabel="Price", indixlabel="Time", indiylabel="Deviation rate")
'''