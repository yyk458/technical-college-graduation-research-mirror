library(quantmod)
library(tseries)
#library(TTR)
library(urca)
#library(forecast)
library(RMySQL)
db = dbDriver("MySQL")
con = dbConnect(db, dbname="BTCJPYbitFlyer", user="BTCminer", host="127.0.0.1", password="")
BTC = dbGetQuery(con, "select * from 5minute where datetime > '2018-11-01 12:00:00' and datetime < '2018-11-02 12:00:00'")
#day = as.Date(BTC1d$datetime)
BTC = BTC[2:7]
#print(BTC)
BTC$open = BTC$open/1000
BTC$high = BTC$high/1000
BTC$low = BTC$low/1000
BTC$close = BTC$close/1000
#print(BTC)
BTC = as.xts(read.zoo(BTC))
#BTC = read.zoo(BTC)
#print(BTC)
#class(BTC)
#par(mfcol=c(2,2))
chartSeries(BTC, type="candlesticks", theme=chartTheme('white', up.col='red',dn.col='blue'))

system("mv Rplots.pdf drowing01.pdf")
cat("done.\n")