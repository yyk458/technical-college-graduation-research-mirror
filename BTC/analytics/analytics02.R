library(tseries)
#library(TTR)
library(urca)
#library(forecast)
library(RMySQL)
db = dbDriver("MySQL")
con = dbConnect(db, dbname="BTCJPYbitFlyer", user="BTCminer", host="127.0.0.1", password="")
BTC1d = dbGetQuery(con, "select * from 1day where datetime > '2018-09-20 00:00:00' and datetime < '2018-10-25 00:00:00'")
day = as.Date(BTC1d$datetime)
price1d = BTC1d$close
logprice1d = log(price1d)
return1d = diff(logprice1d)*100

#描画
par(mfcol=c(2,2))
#価格
par(xaxt="n")
plot(day, price1d, type="l", main="Price of BTCJPY", xlab="time", ylab="", lab=c(15,7,0), las=1)
par(xaxt="s")
axis.Date(1, at=seq(min(day),max(day),"months"), format="%m/%d")
#収益率
par(xaxt="n")
plot(day[2:length(day)], return1d, type="l", main="BTCJPY\'s rate of return", xlab="time", ylab="", lab=c(10,7,6), las=1)
par(xaxt="s")
axis.Date(1, at=seq(min(day),max(day),"months"), format="%m/%d")



#気を取り直して単位根検定
adf.test(price1d)
adf.test(return1d)

#コレログラム
#png("correlogram_btc1dr.png", width=2560, height=1280)
par(mfcol=c(2,1))
#pdf("BTCJPYcorrelogram.pdf")
acfs = acf(return1d, plot=F)
plot(acfs, main="BTCJPY\'s correlogram")
#plot(acfs, main="BTCJPY\'s correlogram")
#dev.off()
#ARモデル
ar(return1d, aic=F)


system("mv Rplots.pdf analytics02.pdf")
cat("\n")