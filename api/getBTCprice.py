#coding: utf-8

#標準出力(stdout)をcsvファイルにリダイレクトしてください．
#sys.stderr.writeはただの標準エラー出力によるログなので消しても動く．
import sys
import urllib.request
from datetime import datetime, timedelta, timezone

if len(sys.argv) != 2 or (sys.argv[1] != "1m" and sys.argv[1] != "5m" and sys.argv[1] != "1h" and sys.argv[1] != "4h" and sys.argv[1] != "1d"):
    sys.stderr.write("コマンドライン引数が不正です．\npython3 getBTCprice.py [periods(\"1m\" or \"5m\" or \"1h\" or \"4h\" or \"1d\")] > [csvfile]\n")
    sys.exit()

#timezone
JST = timezone(timedelta(hours=+9), 'JST')

#範囲入力
sys.stderr.write("start year month day?>")
stdata = [int(i) for i in input().split(' ')]
sys.stderr.write("If you want data until present time, you need to input only '0'.\nend year month day?>")
etdata = [int(i) for i in input().split(' ')]

#取引所等パラメタ指定
market = "bitflyer/"
pricetype = "btcjpy/"
periodslist = {"1m":"60", "5m":"300", "1h":"3600", "4h":"14400", "1d":"86400"}
periods = ""#足間隔
after = datetime.now(JST)#ここから(ほんの初期化)
before = datetime.now(JST).timestamp()#ここまで

#範囲・間隔・url指定
after = datetime(stdata[0], stdata[1], stdata[2], 0, 0, 0, 0, JST).timestamp()
if etdata[0] != 0:
    before = datetime(etdata[0], etdata[1], etdata[2], 0, 0, 0, 0, JST).timestamp()

periods = periodslist[sys.argv[1]]
url = "https://api.cryptowat.ch/markets/" + market + pricetype + "ohlc?periods=" + periods + "&after=" + str(int(after)) + "&before=" + str(int(before))

#ただのログ
sys.stderr.writelines("after:" + str(datetime.fromtimestamp(after)) + "(" + str(after) + ")" + "\n")
sys.stderr.writelines("before:" + str(datetime.fromtimestamp(before)) + "(" + str(before) + ")" + "\n")
sys.stderr.write(url + "\n")

#apiにリクエストを送信し，レスポンスをcsv形式に変換し標準出力する．
with urllib.request.urlopen(url) as response:
    row = str(response.read().decode("utf-8"))
    row = row.split(":")
    dat = row[2]
    dat = dat.replace("[", "")
    dat = dat.split("],")
    dat.pop(-1)
    print("time,start,high,low,close,Volume")
    for i in dat:
        data = i.split(",")
        data[0] = str(datetime.fromtimestamp(int(data[0])))
        dt = data[0].split(" ")
        #なんかたまに価格取得できないときあるからそれは飛ばす．
        if data[1] == "0" or data[2] == "0" or data[3] == "0" or data[4] == "0":
            pass
        #たまにどっから取ってきたかもわからないようなメンテ中のデータを引っ張って来ることがあるのでそれも飛ばす．
        elif dt[1] == "04:05:00" or dt[1] == "04:10:00":
            pass
        else:
            print(data[0] + "," + data[1] + "," + data[2] + "," + data[3] + "," + data[4] + "," + data[5])
    status = response.getcode()
    sys.stderr.write("Status code: " + str(status) + "\n")
    headers = response.info()
    sys.stderr.write(str(headers))


#API仕様: https://cryptowatch.jp/docs/api