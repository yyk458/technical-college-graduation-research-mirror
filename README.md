# technical-college-graduation-research-mirror
テクニカル 高専 卒業 研究 鏡

## api/
あぴ ディレクトリ　には，BTC価格データを手に入れるするプログラムと，BTC価格データを，DBに挿入するプログラムがあります．
BTC価格を得るために使用されたpythonのバージョンは3.6.4です。
### getBTCprive.py
手に入れる BTC 価格 .py は，[Cryptowatch](https://cryptowatch.jp/docs/api) (泣く p に 見る)というapiを使うて，BTC価格データを手に入れるします．

あなたは，間隔は，1分，5分，1時間，4時間，1日から選ぶできます．

あなたは，期間を指定するできます．また，

注意しなさい，それは不可能です，もしもあなたが短い間隔を選びました，過去すぎるデータを手に入れるする．

### insertDB_add.py
挿入 DB 追加 .pyは，保存されているcsvフォーマットで，BTCの価格データを，DBに挿入するします．

## BTC/
BTCディレクトリには，BTC価格データを分析するプログラムがあります．

### statistical_test/
統計検定 ディレクトリは，BTC価格データを統計検定します．

使用言語はRです．

私は，パッケージtseriesとRMySQLを使うしました．

### analytics/
分析学 ディレクトリは，BTC価格データへの時系列分析です．

使用言語はRです．

私は，パッケージtseriesとRMySQLを使うしました．

### technical/
無意味

### technical_neo/
テクニカルネオ ディレクトリは，はBTC価格データのテクニカル分析へです。

使用言語はpythonです．

それをするために使用されたpythonのバージョンはアナコンダ3-5.1.0です．

図書館[TA-Lib](https://github.com/mrjbq7/ta-lib) (ターィb)が使用されました．テクニカル分析に，

#### technicalkit.py
テクニカルキット .pyは，私の図書館です．

## data/
だた ディレクトリは，BTC価格データのSQLファイルがあるます．
実行すると，データベースを再現されます．
