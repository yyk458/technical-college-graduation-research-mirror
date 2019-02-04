# -*- coding: utf-8 -*-
from datetime import datetime, timedelta, timezone
import MySQLdb
import sys
import numpy as np
import pandas as pd
import talib
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import statsmodels.api as sm
import technicalkit #自作ライブラリ

'''
xt = [10,20,30,40,50,20,40,60,80,100]
sma = talib.SMA(np.array(xt, dtype='f8'), timeperiod=5)
ema = talib.EMA(np.array(xt, dtype='f8'), timeperiod=5)
print(sma)
print(ema)
'''

'''
fp = FontProperties(fname=r'/System/Library/Fonts/ヒラギノ明朝 ProN W3.ttc', size=15)
n = 200

x = np.random.random(n)
y = np.random.random(n)

ax = plt.subplot()
ax.plot(x, y, color='black')
plt.title(u"まんげ！", fontproperties=fp)
plt.show()
'''

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
npprices = np.array(prices, dtype='f8')
npvolumes = np.array(volumes, dtype='f8')
#SMA
smavsr = talib.SMA(npprices, timeperiod=2)
#plt.plot(smavsr)
#plt.show()
technicalkit.plot_withMA(rang, True, npprices, [smavsr], ['red'], ["SMA2"])
#対数差分
logdiff = np.log(smavsr[1:]) - np.log(smavsr[:-1])
print(logdiff)
#plt.plot(logdiff)
#plt.show()
acf = sm.tsa.stattools.acf(logdiff[1:])
print(acf)

#自己相関
fig = plt.figure(figsize=(12,8))
ax = fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf(logdiff[1:], lags=40, ax=ax)
plt.show()