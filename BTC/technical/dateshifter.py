#coding: utf-8
from datetime import datetime, timedelta, timezone
import MySQLdb
import csv
import sys

s = "2018-10-30 12:00:00"
e = "2018-11-02 23:55:00"
sdate = datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
edate = datetime.strptime(e, '%Y-%m-%d %H:%M:%S')
months = 30
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
yearmonth = "201811"
for i in range(months):
    fname = "data/" + yearmonth + "/data" + str(i) + ".csv"
    fp = open(fname, "w")
    sql = "SELECT datetime,close,volume FROM 5minute WHERE datetime >= \'%s\' AND datetime <= \'%s\'" % (s, e)
    cur.execute(sql)
    dat = cur.fetchall()
    #print(type(dat))
    fp.write("datetime,close,volume\n")
    for row in dat:
        #print(row)
        #times = row[0]
        times = row[0].strftime("%Y-%m-%d %H:%M:%S")
        close = str(row[1])
        volume = str(row[2])
        fp.write(times + "," + close + "," + volume + "\n")

    sys.stderr.write("\n")
    sdate = sdate + timedelta(days=1)
    edate = edate + timedelta(days=1)
    s = sdate.strftime("%Y-%m-%d %H:%M:%S")
    e = edate.strftime("%Y-%m-%d %H:%M:%S")
    sys.stderr.write(s)
    sys.stderr.write("\n")
    sys.stderr.write(e)
    sys.stderr.write("\n")
    fp.close()

sys.stderr.write("\n")
#保存しないと操作が反映されない．
#一応ね
conn.commit()
conn.close()