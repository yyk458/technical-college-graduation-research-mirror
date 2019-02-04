library(quantmod)
library(tseries)
#library(TTR)
library(urca)
library(forecast)
library(RMySQL)
db = dbDriver("MySQL")
con = dbConnect(db, dbname="BTCJPYbitFlyer", user="BTCminer", host="127.0.0.1", password="")
BTC = dbGetQuery(con, "select datetime,close,volume from 5minute where datetime >= '2018-10-31 12:00:00' and datetime <= '2018-11-30 23:55:00'")
#応急処置:最新版では対応
#BTC = BTC[-4754,]
#BTC = BTC[-5325,]
#BTC = BTC[-5897,]
#BTC = BTC[-7613,]
#print(BTC)

BTC_p = BTC$close
volume = BTC$volume
p_log = log(BTC_p)#対数価格です
BTC_r = diff(p_log)#対数差収益率
par(mfcol=c(2,1))
plot(BTC_p, type="l", main="BTC5m")
barplot(volume, main="BTC5m's Volume")
plot(BTC_p, type="l", main="BTC5m")
plot(BTC_r, type="l", main="return of BTC5m")
#単位根検定
adf.test(BTC_p)
adf.test(BTC_r)
cat("\n")

#自己相関
par(mfcol=c(1,1))
acf(BTC_r, plot=T)
acf(BTC_r, plot=T, type="p")
acf(BTC_r, plot=F)
acf(BTC_r, plot=F, type="p")


#AR
cat("\n\nAR\n\n")
#t = ar(BTC_r, aic=T, order.max=3)
#print(t)

fit20 = arima(BTC_r, order=c(20,0,0))
#fit3 = arima(BTC_r, order=c(3,0,0))
#fit1 = arima(BTC_r, order=c(1,0,0))
fit0 = arima(BTC_r, order=c(0,0,0))
print(fit20)
#print(fit3)
#print(fit1)
print(fit0)



system("mv Rplots.pdf technical01.pdf")
system("open technical01.pdf")
cat("done.\n")