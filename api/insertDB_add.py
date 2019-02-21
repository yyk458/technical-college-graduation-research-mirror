#coding: utf-8
#csvに溜め込んだデータをDBに接続し挿入する．
#プログラムを統合すればいい話だがそれすら面倒くさい．
#自分専用のプログラムであり汎用性を持たせるつもりはない．
import MySQLdb#pip install mysqlclient
import sys
from getpass import getpass
import csv
from datetime import datetime

n = len(sys.argv)

#頑なにstderrストリームに出力させようとするyyk458さん
if n <= 1:
    sys.stderr.write("コマンドライン引数が不正です．\n")
    sys.exit()

#対象ファイルのインデックスは1からであることに注意
files = []
for i in sys.argv:
    files.append(i)

host = "localhost"
dbname = "BTCJPYbitFlyer"
charset = "utf8"
user = "BTCminer"
passwd = ""

conn = MySQLdb.connect(db=dbname, host=host, charset=charset, user=user, passwd=passwd)
cur = conn.cursor()

tabledic = {"1d":"1day", "1m":"1minute", "5m":"5minute", "1h":"1hour", "4h":"4hour", "1w":"1week"}
tables = []

#どのテーブルから挿入していくか
for i in range(n-1):
    tmp = sys.argv[i+1].split("_")
    tables.append(tabledic[tmp[2]])

#挿入作業
for i in range(n-1):
    fp = open(sys.argv[i+1], 'r')
    dat = csv.reader(fp)
    header = next(dat)#ヘッダー読み飛ばし
    sql = "SELECT * FROM %s ORDER BY id desc limit 1" % (tables[i])
    cur.execute(sql)
    newest = cur.fetchall()
    newest = newest[0][1]#DBtime
    sys.stderr.write("newest: " + str(newest) + "\n")
    for row in dat:
        row[0] = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
        #最新
        if row[0] > newest:
            for k in range(4):
                row[k+1] = int(row[k+1])
            row[5] = float(row[5])
            sql = u"INSERT INTO %s VALUES(NULL, \'%s\', %s, %s, %s, %s, %s)" % (tables[i], row[0], row[1], row[2], row[3], row[4], row[5])
            cur.execute(sql)

#保存しないと操作が反映されない．
conn.commit()
conn.close()