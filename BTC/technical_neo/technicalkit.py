#coding: utf-8
from datetime import datetime, timedelta, timezone
import MySQLdb
import sys
import copy
import numpy
import pandas
import talib
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

#データは全てnumpy配列であること前提
#まあnumpyでなくpy3標準のリストでも動くとは思うけど

#2つ以上のデータを重ねて書く可能性のある関数は全て凡例の文字列をリストで渡す必要がある．(要はplotrawdata以外)

#font = FontProperties(fname=r'/System/Library/Fonts/ヒラギノ角ゴシック W5.ttc', size=15)

def plotrawdata(rang, isgrid, raw, xlabel="", ylabel="", fontsize=20, saved=False, fname=""):
    plt.rcParams["font.size"] = fontsize
    fig = plt.figure()
    ax = plt.subplot()
    plt.grid(isgrid)
    ax.plot(rang, raw, color='black')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if saved:
        plt.savefig(fname)
    plt.show()

#原系列と移動平均線を任意の数引く
def plot_withMA(rang, isgrid, raw, malist, macolors, malabels, xlabel="", ylabel="", fontsize=20, saved=False, fname=""):
    plt.rcParams["font.size"] = fontsize
    fig = plt.figure()
    ax = plt.subplot()
    plt.grid(isgrid)
    ax.plot(rang, raw, color='black', label="raw")
    for i in range(len(malist)):
        ax.plot(rang, malist[i], color=macolors[i], label=malabels[i])
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.legend()
    if saved:
        plt.savefig(fname)
    plt.show()

#とりあえず指定したデータ全部重ねて描く
def plot_overlap(rang, isgrid, datas, colors, labels, xlabel="", ylabel="", fontsize=20, saved=False, fname=""):
    plt.rcParams["font.size"] = fontsize
    fig = plt.figure()
    ax = plt.subplot()
    plt.grid(isgrid)
    for i in range(len(datas)):
        ax.plot(rang, datas[i], color=colors[i], label=labels[i])
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.legend()
    if saved:
        plt.savefig(fname)
    plt.show()

#インジケータも描画
def plot_with_indicator(rang, isgrid, updatas, upcolors, uplabels, indicators, indicolors, indilabels, upxlabel="", upylabel="", indixlabel="", indiylabel="", fontsize=20, saved=False, fname=""):
    plt.rcParams["font.size"] = fontsize
    fig = plt.figure()
    ax1 = plt.subplot2grid((2,2), (0,0), colspan=2)
    ax2 = plt.subplot2grid((2,2), (1,0), colspan=2)
    ax1.grid(isgrid)
    ax2.grid(isgrid)
    for i in range(len(updatas)):
        ax1.plot(rang, updatas[i], color=upcolors[i], label=uplabels[i])
    ax1.set_xlabel(upxlabel)
    ax1.set_ylabel(upylabel)
    for i in range(len(indicators)):
        ax2.plot(rang, indicators[i], color=indicolors[i], label=indilabels[i])
    ax2.set_xlabel(indixlabel)
    ax2.set_ylabel(indiylabel)
    ax1.legend()
    ax2.legend()
    if saved:
        plt.savefig(fname)
    plt.show()
    

#短期長期2つのMA線からGC,DCのインデックスを検出
def MAcross(mashr, malng):
    cross = {"GC":None, "DC":None}
    crosses = []
    for i in range(len(mashr) - 2):
        if (mashr[i] - malng[i] < 0) and (mashr[i+1] - malng[i+1] > 0):
            cross["GC"] = i + 1
        elif (mashr[i] - malng[i]) - (mashr[i+1] - malng[i+1]) == 0:
            if (mashr[i] - malng[i] < 0) and (mashr[i+2] - malng[i+2] > 0):
                cross["GC"] = i + 1

        elif (mashr[i] - malng[i] > 0) and (mashr[i+1] - malng[i+1] < 0):
            cross["DC"] = i + 1
        elif (mashr[i] - malng[i]) - (mashr[i+1] - malng[i+1]) == 0:
            if (mashr[i] - malng[i] > 0) and (mashr[i+2] - malng[i+2] < 0):
                cross["DC"] = i + 1
        
        if (cross["GC"] != None) and (cross["DC"] != None):
            crosses.append(copy.deepcopy(cross))#Important!!!!!
            cross["GC"] = None
            cross["DC"] = None

    return crosses

#たまにDCが最初に来るので最初のDCを飛ばしてGCからのリストにする
def XConverter(crosslist):
    newcrosslist = []
    cross = {"GC":None, "DC":None}
    if crosslist[0]["GC"] > crosslist[0]["DC"]:
        for i in range(len(crosslist) - 1):
            cross["GC"] = crosslist[i]["GC"]
            cross["DC"] = crosslist[i+1]["DC"]
            newcrosslist.append(copy.deepcopy(cross))
        return newcrosslist
    else:
        return crosslist

#DC(売りシグナル)からのリストにする
#早く実装しろ

#係数一般化MA
#早く実装しろ

#買い・売りシグナル(交差点)より売買結果を返す
#MAcrossとか書いてるけど別に買い・売りシグナルが必ず交互にくるテクニカル指標ならこの関数使えばok
def MAcross_trading(crosslist, raw):
    result = []
    for i in range(len(crosslist)):
        amount = int(raw[crosslist[i]["DC"]] - raw[crosslist[i]["GC"]]) #損益額
        rate = raw[crosslist[i]["DC"]] / raw[crosslist[i]["GC"]] #損益率
        iswon = amount > 0 #勝敗
        res = {"amount":amount, "rate":rate, "iswon":iswon}
        result.append(copy.deepcopy(res))
    return result

#MA乖離率計算
def MAdeviationrate(raw, ma):
    dev = []
    for i in range(len(raw)):
        dev.append((raw[i]-ma[i]) / ma[i])
    return numpy.array(dev, dtype='f8')

#乖離率の書い売りシグナルを返す
#ここで返すリストは買い・売り両方から入る
def MAdevpoint(madev, buy_th, sell_th):
    point = {"GC":None, "DC":None}
    points = []
    for i in range(len(madev)):
        if madev[i] <= buy_th and point["GC"] == None:
            point["GC"] = i
        elif madev[i] >= sell_th and point["DC"] == None:
            point["DC"] = i

        if (point["GC"] != None) and (point["DC"] != None):
            points.append(copy.deepcopy(point))#Important!!!!!
            point["GC"] = None
            point["DC"] = None
    
    return points

#MA乖離率をはじめとした，買い・売りシグナルが連続して発生する可能性のあるテクニカル指標に対して，売買結果を返す
def MAdev_trading(points, raw, startwithselling=False):
    result = []
    for i in range(len(points)):
        istrade = False
        amount = int(raw[points[i]["DC"]] - raw[points[i]["GC"]])
        
        if points[i]["GC"] > points[i]["DC"] and startwithselling:
            print("売りから入った結果をどうぞ")
            amount = amount * (-1)#損益額反転で解決
            rate = raw[points[i]["GC"]] / raw[points[i]["DC"]]
            istrade = True
        elif points[i]["GC"] < points[i]["DC"]:
            rate = raw[points[i]["DC"]] / raw[points[i]["GC"]]
            istrade = True

        if istrade:
            iswon = amount > 0
            res = {"amount":amount, "rate":rate, "iswon":iswon}
            result.append(copy.deepcopy(res))

    return result

#売買結果をそれなりに分析
def analize_trading_result(result, isprint=True):
    tradenum = len(result)
    sumamount = 0
    rate = 0
    wonnum = 0
    for i in range(tradenum):
        sumamount += result[i]["amount"]
        rate += result[i]["rate"]
        wonnum += result[i]["iswon"]
    totalrate = rate / tradenum
    wonrate = wonnum / tradenum
    if isprint:
        print("売買回数: " + str(tradenum) + "\n損益合計: " + str(sumamount) + "\n合計収益率: " + str(totalrate) + "\n勝利回数: " + str(wonnum) + "\n勝率: " + str(wonrate))
    return {"tradenum":tradenum, "total":sumamount, "totalrate":totalrate, "wonnum":wonnum, "wonrate":wonrate}
