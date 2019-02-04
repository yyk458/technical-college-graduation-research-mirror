#coding: utf-8
from datetime import datetime, timedelta, timezone
import MySQLdb
import sys
import numpy as np
import pandas as pd
import talib
import matplotlib.pyplot as plt
import statsmodels.api as sm
from scipy.stats import norm
import technicalkit #自作ライブラリ

s = "2018-11-27 20:00:00"
e = "2018-11-29 18:00:00"
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
#sql = "SELECT datetime,close,volume FROM 1day WHERE datetime >= \'%s\' AND datetime <= \'%s\'" % ("2018-07-14 00:00:00", "2018-11-14 12:00:00")
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
npprices = np.array(prices, dtype='f8')
npvolumes = np.array(volumes, dtype='f8')
#対数差分
#logdiff = numpy.log(npprices[1:]) - numpy.log(npprices[:-1])
#print(logdiff)
#sma = talib.SMA(npprices, timeperiod=25)
#wma = talib.WMA(npprices, timeperiod=25)
#ema = talib.EMA(npprices, timeperiod=50)

#malist = [sma, wma]#, ema]
#macolor = ['red','blue']#,'blue']
#malabel = ["SMA","WMA"]#,"EMA"]

#technicalkit.plot_withMA(rang, True, npprices, malist, macolor, malabel, xlabel="Time", ylabel="Price")

#technicalkit.plotrawdata(rang, True, npprices, xlabel=u"Time", ylabel=u"Price")
#technicalkit.plotrawdata(range(len(times)-1), True, numpy.array(logdiff), xlabel=u"Time", ylabel=u"Return rate")

#単位根検定
#adftest_price = sm.tsa.adfuller(npprices)
#adftest_return = sm.tsa.adfuller(logdiff)
#print(adftest_price)
#print(adftest_return)

n = np.linspace(-5.0, 5.0, 10000)

# 平均0, 標準偏差1の正規分布における、xの確率を求める
p = []
for i in range(len(n)):
    p.append(norm.pdf(x=n[i], loc=0, scale=1))

# 乱数－確率 の特性を散布図で表し、標準正規分布のグラフを作成
plt.scatter(n, p)
plt.show()