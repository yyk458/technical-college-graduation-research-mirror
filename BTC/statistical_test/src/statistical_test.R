library(tseries)
library(urca)
library(forecast)
csv1d = "../../../api/downloads/1d/BTCJPY_bitFlyer_1d_all.csv"
csv5m = "../../../api/downloads/5m/BTCJPY_bitFlyer_5m_201810.csv"
csv1m = "../../../api/downloads/1m/BTCJPY_bitFlyer_1m_201810.csv"
csv1h = "../../../api/downloads/1h/BTCJPY_bitFlyer_1h_201809_201810.csv"
csv4h = "../../../api/downloads/4h/BTCJPY_bitFlyer_4h_201809_201810.csv"
btc1d = read.csv(csv1d, fileEncoding="UTF-8")
btc5m = read.csv(csv5m, fileEncoding="UTF-8")
btc1m = read.csv(csv1m, fileEncoding="UTF-8")
btc1h = read.csv(csv1h, fileEncoding="UTF-8")
btc4h = read.csv(csv4h, fileEncoding="UTF-8")

#分足は一日
btc5m = btc5m[3147:3432,]
btc1m = btc1m[1:1406,]

#日足
price1d = btc1d$close
#対数価格
logprice1d = log(price1d)
#対数差収益率
return1d = diff(logprice1d)*100
par(mfcol=c(2,1))
plot(price1d, type="l", main="price1d")
plot(return1d, type="l", main="return1d")
#平均・標準偏差
mean_btc1dr = mean(return1d)
sd_btc1dr = sd(return1d)
cat("mean1dr:", mean_btc1dr, "\n")
cat("sd1dr:", sd_btc1dr, "\n")
#ヒストグラム
par(mfcol=c(1,1))
hist(return1d, main="return1d", breaks=seq(-15,15,1))


#5分足
price5m = btc5m$close
#対数価格
logprice5m = log(price5m)
#対数差収益率
return5m = diff(logprice5m)*100
par(mfcol=c(2,1))
plot(price5m, type="l", main="price5m")
plot(return5m, type="l", main="return5m")
#平均・標準偏差
mean_btc5mr = mean(return5m)
sd_btc5mr = sd(return5m)
cat("mean5mr:", mean_btc5mr, "\n")
cat("sd5mr:", sd_btc5mr, "\n")
#ヒストグラム
par(mfcol=c(1,1))
hist(return5m, main="return5m", breaks=seq(-1.0,1.0,0.05))


#1分足
price1m = btc1m$close
#対数価格
logprice1m = log(price1m)
#対数差収益率
return1m = diff(logprice1m)*100
par(mfcol=c(2,1))
plot(price1m, type="l", main="price1m")
plot(return1m, type="l", main="return1m")
#平均・標準偏差
mean_btc1mr = mean(return1m)
sd_btc1mr = sd(return1m)
cat("mean1mr:", mean_btc1mr, "\n")
cat("sd1mr:", sd_btc1mr, "\n")
#ヒストグラム
par(mfcol=c(1,1))
hist(return1m, main="return1m", breaks=seq(-0.8,0.8,0.05))


#1時間足
price1h = btc1h$close
#対数価格
logprice1h = log(price1h)
#対数差収益率
return1h = diff(logprice1h)*100
par(mfcol=c(2,1))
plot(price1h, type="l", main="price1h")
plot(return1h, type="l", main="return1h")
#平均・標準偏差
mean_btc1hr = mean(return1h)
sd_btc1hr = sd(return1h)
cat("mean1hr:", mean_btc1hr, "\n")
cat("sd1hr:", sd_btc1hr, "\n")
#ヒストグラム
par(mfcol=c(1,1))
hist(return1h, main="return1h", breaks=seq(-6,6,0.5))


#4時間足
price4h = btc4h$close
#対数価格
logprice4h = log(price4h)
#対数差収益率
return4h = diff(logprice4h)*100
par(mfcol=c(2,1))
plot(price4h, type="l", main="price4h")
plot(return4h, type="l", main="return4h")
#平均・標準偏差
mean_btc4hr = mean(return4h)
sd_btc4hr = sd(return4h)
cat("mean4hr:", mean_btc4hr, "\n")
cat("sd4hr:", sd_btc4hr, "\n")
#ヒストグラム
par(mfcol=c(1,1))
hist(return4h, main="return4h", breaks=seq(-8,8,0.5))


#正規分布か?
cat("\n正規分布か？\n")
shapiro.test(return1d)
shapiro.test(return5m)
shapiro.test(return1m)
shapiro.test(return1h)
shapiro.test(return4h)


#単位根検定
#Dickey-Fuller検定(帰無仮説：データ系列に単位根が存在する)
#価格そのもの
cat("\n単位根が存在するか？\n")
cat("価格そのもの\n")
adf.test(price1d)
adf.test(price5m)
adf.test(price1m)
adf.test(price1h)
adf.test(price4h)
#対数差収益率
cat("対数差収益率\n")
adf.test(return1d)
adf.test(return5m)
adf.test(return1m)
adf.test(return1h)
adf.test(return4h)

#KPSS検定(帰無仮説：データ系列に単位根が存在しない：差分を取る必要はない)
cat("\n差分を取る必要はあるか？\n")
summary(ur.kpss(logprice1d))
summary(ur.kpss(logprice5m))
summary(ur.kpss(logprice1m))
summary(ur.kpss(logprice1h))
summary(ur.kpss(logprice4h))
#ndiffsで差分を取るべき回数がわかる．
cat("\n差分を取る必要があるなら何階差分を取るべきか？\n")
ndiffs(logprice1d)
ndiffs(logprice5m)
ndiffs(logprice1m)
ndiffs(logprice1h)
ndiffs(logprice4h)
cat("\n対数価格の差分に対して同検定をする．\n")
summary(ur.kpss(return1d))
summary(ur.kpss(return5m))
summary(ur.kpss(return1m))
summary(ur.kpss(return1h))
summary(ur.kpss(return4h))


#独立した標本か？
cat("\n独立した標本か？\n")
b_r1d = as.factor(return1d < mean(return1d))
b_r5m = as.factor(return5m < mean(return5m))
b_r1m = as.factor(return1m < mean(return1m))
b_r1h = as.factor(return1h < mean(return1h))
b_r4h = as.factor(return4h < mean(return4h))
runs.test(b_r1d)
runs.test(b_r5m)
runs.test(b_r1m)
runs.test(b_r1h)
runs.test(b_r4h)

#自己共分散
acf(return1d, plot=F, type="cov")
acf(return5m, plot=F, type="cov")
acf(return1m, plot=F, type="cov")
acf(return1h, plot=F, type="cov")
acf(return4h, plot=F, type="cov")
#自己相関係数
acf(return1d, plot=T)
par(mfcol=c(2,2))
acf(return5m, plot=T)
acf(return1m, plot=T)
acf(return1h, plot=T)
acf(return4h, plot=T)
#偏自己相関係数
par(mfcol=c(1,1))
acf(return1d, plot=T, type="p")
par(mfcol=c(2,2))
acf(return5m, plot=T, type="p")
acf(return1m, plot=T, type="p")
acf(return1h, plot=T, type="p")
acf(return4h, plot=T, type="p")


#ARモデルに当てはまる？
ar(price1d, aic=T)
ar(price5m, aic=T)
ar(price1m, aic=T)
ar(price1h, aic=T)
ar(price4h, aic=T)
ar(return1d, aic=T)
ar(return5m, aic=T)
ar(return1m, aic=T)
ar(return1h, aic=T)
ar(return4h, aic=T)


system("mv Rplots.pdf statistical_test.pdf")
cat("\n")