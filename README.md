# technical-college-graduation-research-mirror
テクニカル 高専 卒業 研究 鏡

## api/
あぴ ディレクトリ　には，BTC価格データを手に入れるするプログラムと，BTC価格データを，DBに挿入するプログラムがあります．
### getBTCprive.py
手に入れる BTC 価格 .py は，[Cryptowatch](https://cryptowatch.jp/docs/api) (泣く p に 見る)というapiを使うて，BTC価格データを手に入れるします．

あなたは，間隔は，1分，5分，1時間，4時間，1日から選ぶできます．

期間を指定するできます．

注意しなさい，それは不可能です，もしもあなたが短い間隔を選びました，過去すぎるデータを手に入れるする．

### insertDB_add.py
挿入 DB 追加 .pyは，保存されているcsvフォーマットで，BTCの価格データを，DBに挿入するします．

## BTC
BTCディレクトリには，BTC価格データを分析するプログラムがあります．

### statistical_test/
統計検定 ディレクトリは，BTC価格データを統計検定します．

### analytics/
分析学 ディレクトリは，BTC価格データへの時系列分析です．

### technical/
無意味

### technical_neo/
テクニカルネオ ディレクトリは，はBTC価格データのテクニカル分析へです。

#### technicalkit.py
テクニカルキット .pyは，私の図書館です．
