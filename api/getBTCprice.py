#coding: utf-8

#sys.stderr.writeはただの標準エラー出力によるログなので消しても動く．
import sys
import urllib.request
from datetime import datetime, timedelta, timezone
import MySQLdb#pip install mysqlclient
import json

#python3 getBTCprice.py [peridos] [after(YYYY-mm-dd/0)] [before(YYYY-mm-dd/0)] [csvfile]

if len(sys.argv) != 5 or (sys.argv[1] != "1m" and sys.argv[1] != "5m" and sys.argv[1] != "1h" and sys.argv[1] != "4h" and sys.argv[1] != "1d" and sys.argv[1] != "1w"):
    sys.stderr.write("コマンドライン引数が不正です．\n")
    sys.exit()


#DB情報(範囲指定時に使用)
host = "localhost"
dbname = "BTCJPYbitFlyer"
charset = "utf8"
user = "BTCminer"
passwd = ""
conn = MySQLdb.connect(db=dbname, host=host, charset=charset, user=user, passwd=passwd)
cur = conn.cursor()

tabledic = {"1d":"1day", "1m":"1minute", "5m":"5minute", "1h":"1hour", "4h":"4hour", "1w":"1week"}

#timezone
JST = timezone(timedelta(hours=+9), 'JST')

#取引所等パラメタ指定
market = "bitflyer/"
pricetype = "btcjpy/"
periodslist = {"1m":"60", "5m":"300", "1h":"3600", "4h":"14400", "1d":"86400", "1w":"604800"}
periods = ""#足間隔

after = datetime.now(JST).timestamp()#ほんの初期化
#ここから
if sys.argv[2] == "0":
    #DB上の最新の日付を取得
    sql = "SELECT * FROM %s ORDER BY id desc limit 1" % (tabledic[sys.argv[1]])
    cur.execute(sql)
    newest = cur.fetchall()
    after = newest[0][1].timestamp()#デフォルトはDB上の最新時刻
else:
    tstr = sys.argv[2].split("-")
    after = datetime(int(tstr[0]), int(tstr[1]), int(tstr[2]), 0, 0, 0, 0, JST).timestamp()#コマンドライン引数の日付

#ここまで
before = datetime.now(JST).timestamp()#デフォルトは現在時刻
if sys.argv[3] != "0":
    tstr = sys.argv[3].split("-")
    before = datetime(int(tstr[0]), int(tstr[1]), int(tstr[2]), 0, 0, 0, 0, JST).timestamp()#コマンドライン引数の日付

#範囲・間隔・url指定
periods = periodslist[sys.argv[1]]
url = "https://api.cryptowat.ch/markets/" + market + pricetype + "ohlc?periods=" + periods + "&after=" + str(int(after)) + "&before=" + str(int(before))

#ただのログ
sys.stderr.writelines("after:" + str(datetime.fromtimestamp(after)) + "(" + str(after) + ")" + "\n")
sys.stderr.writelines("before:" + str(datetime.fromtimestamp(before)) + "(" + str(before) + ")" + "\n")
sys.stderr.write(url + "\n")

#apiにリクエストを送信し，レスポンスをcsv形式に変換し標準出力する．
with urllib.request.urlopen(url) as response:
    dat = response.read().decode("utf-8")#type(dat)=str
    dat = json.loads(dat)#type(dat)=dict
    rows = dat['result'][periods]#type(rows)=list
    #売買代金を除いてcsvに出力したい．
    fp = open(sys.argv[4], "w")
    fp.write("time,start,high,low,close,Volume\n")
    for row in rows:#type(row)=list[int,int,int,int,int,float,float]
        #print(row)
        dt = str(datetime.fromtimestamp(row[0])).split(" ")
        #価格取得失敗時には飛ばす
        if row[1] == 0 or row[2] == 0 or row[3] == 0 or row[4] == 0:
            pass
        #メンテ中の謎データは飛ばす
        elif dt[1] == "04:05:00" or dt[1] == "04:10:00":
            pass
        else:
            fp.write(str(datetime.fromtimestamp(row[0])) + "," + str(int(row[1])) + "," + str(int(row[2])) + "," + str(int(row[3])) + "," + str(int(row[4])) + "," + str(row[5]) + "\n")
    
    status = response.getcode()
    sys.stderr.write("Status code: " + str(status) + "\n")
    headers = response.info()
    sys.stderr.write(str(headers))


#API仕様: https://cryptowatch.jp/docs/api