# BitMexLineNotifyBot

## 概要
 BitMexの資産を監視してLINEに通知するBotです。  
 β版の為、不具合がある場合があります。  
 不具合を発見した場合は連絡を頂けると助かります。  
 また、ベースにしたコードから不要なコードが残っている場合がありますが、動作には影響ありません。  
 これをベースに改変する場合は注意してください。
 資産やポジションを監視して通知するだけなので、勝手に注文/注文キャンセルしたり出金する事はありません。

## 仕様
* Bot起動時に起動通知と現在の資産情報を通知
* 数秒毎(デフォルト:6秒)にポジション情報を取得
* ポジションを持つ、ポジションに変更がある、ポジションを決済するタイミングでLINE通知
* 決済(=ポジション無し)した場合はイン - アウトの差分を見て損益を通知
* XBT/USDのみ対応、その他通貨ペアは未対応

## 通知する項目
* 合計資産(XBT)  
* 使用済み資産(XBT)  
* 使用可能資産(XBT)  
* ポジションのサイズ(USD)  
* ポジションの値(XBT)  
* 参入価格(USD)  
* 精算価格(USD)  
* 証拠金(XBT)  
* 未実現損益(XBT:ROE%)  
* 実現損益(XBT)  

※ポジションサイズの-記号はショート、-が無ければロング  

<img src="https://github.com/cryptocat-miner/BitMexLineNotifyBot/blob/master/images/line_notify_1.jpg" width="320px" alt="LINE通知1">
<img src="https://github.com/cryptocat-miner/BitMexLineNotifyBot/blob/master/images/line_notify_2.jpg" width="320px" alt="LINE通知2">
<img src="https://github.com/cryptocat-miner/BitMexLineNotifyBot/blob/master/images/line_notify_3.jpg" width="320px" alt="LINE通知3">
<img src="https://github.com/cryptocat-miner/BitMexLineNotifyBot/blob/master/images/line_notify_4.jpg" width="320px" alt="LINE通知4">  

### 取引履歴通知の追加
資産情報の他に取引履歴を通知するようにしました。
Funding情報も通知します。
* 方向:ショート/ロング
* タイプ:成行/指値/ストップ成行/利食い成行/利食い指値/精算
* 取引量
* 取引価格:成行などで複数回に分かれる場合は1回にまとめて平均価格を通知する
* 取引手数料:+/-
  
<img src="https://github.com/cryptocat-miner/BitMexLineNotifyBot/blob/master/images/trade_notify.jpg" width="320px" alt="取引通知">  


## 開発言語・稼働環境
* 開発言語:Python
* Python環境がインストールされた自身のPCにコードを配置して稼働(Visual Studioでも動作可能)
* Cloud9(AWSのサービス)にコードを配置して稼働
* その他Pythonが動作するクラウドサービス、環境にコードを配置して稼働

## AWS Cloud9での設定方法
24時間監視する場合はAWSのCloud9に配置する方法が無償利用枠を使え、安価で簡単です。
まずはAWSアカウントを作成し、マネジメントコンソールにサインインします。

### Cloud9環境の作成・設定
* マネジメントコンソールの検索窓にCloud9と入れて進みます。
<img src="https://github.com/cryptocat-miner/BitMexLineNotifyBot/blob/master/images/search_cloud9.png" width="320px" alt="search_cloud9">

* Create environmentをクリックします。  
<img src="https://github.com/cryptocat-miner/BitMexLineNotifyBot/blob/master/images/create_cloud9.png" width="320px" alt="create_cloud9">

* 任意の名前を入れてNext Stepをクリックします。
<img src="https://github.com/cryptocat-miner/BitMexLineNotifyBot/blob/master/images/name_environment.png" width="320px" alt="create_cloud9">  

* Cost-saving settingsはコスト低減の為に自動でシャットダウンするまでの時間です。  
24時間監視をしたい場合はNeverを設定してください。  
その他は基本的にはデフォルトの設定で問題ありません。  
Instance typeはt2.microだと無償利用できるはずです。  
設定に問題が無ければNext Stepへ。
<img src="https://github.com/cryptocat-miner/BitMexLineNotifyBot/blob/master/images/configure_settings.png" width="320px" alt="configure_settings">  

* 最後に設定の確認をしてCreate environmentでCloud9のインスタンスが作成されます。  
<img src="https://github.com/cryptocat-miner/BitMexLineNotifyBot/blob/master/images/Review.png" width="320px" alt="Review">  

## Cloud9へのコードの配置・Python設定
以下のファイルをCloud9にドラッグ&ドロップするか、上のメニューバーから  
File -> Upload Local Files...  
を使ってアップロードします。  
ccxtWrapper.py  
LineNotify.py  
LineNotifyBot.py  
orderInfo.py  
orderManager.py  

### Python3設定
右上の歯車を押してプロジェクトの設定を行います。  
<img src="https://github.com/cryptocat-miner/BitMexLineNotifyBot/blob/master/images/project_settings.png" width="320px" alt="project_settings">  

Python SupportのPython Version:をPython3に変更します。  
ちなみにここでもCloud9の自動シャットダウン設定を変更できます。  
<img src="https://github.com/cryptocat-miner/BitMexLineNotifyBot/blob/master/images/python3_settings.png" width="320px" alt="python3_settings">  

次に画面下のコンソールでPython3の設定をします。  
まずはエイリアスをpython3に上書きし、pythonに関連付けるバージョンの選択肢が表示されるので2を選択します。(+が現在の設定)  
```
alias python="python3"
sudo update-alternatives --config python
# 選択肢が表示されたら2を入力してenter.
```
pipのアップグレードを行います。
```
sudo pip install --upgrade pip
```
一応Pythonとpipのバージョンを確認しておきましょう。
```
python -V
pip -V
```
Pythonが3.x.x、pipが19.x.x以上になっていればOKです。
ccxt(BitMexなどの取引所と通信する為のライブラリ)をインストールします。  
```
sudo python3 -m pip install ccxt
```
<img src="https://github.com/cryptocat-miner/BitMexLineNotifyBot/blob/master/images/console.png" width="320px" alt="console">  

これでPython環境とコードの準備ができました。  
後はBitMexとLINE NotifyそれぞれのAPIキーをコピペすれば動かせます。

## LINE NotifyのAPIキー作成と設定
[LINE Notify](https://notify-bot.line.me/ja/) に自分のLINEアカウントでログインし、APIキーを作成します。  

右上の自分の名前 -> マイページ -> アクセストークンの発行(開発者向け) -> トークンを発行する  
で任意のトークン名を入力し、通知を送信するトークルームを選択してください。  
1:1でも作成済のグループでも通知する事ができます。  
ここで設定した名前が通知の際に```[BitMexBot]```のように通知されます。  
発行したAPIキーをコピーし、LineNotify.pyのlineNotifyTokenの""中に貼り付けてください。  
※APIキーはここを離れると見れなくなります。必ずこの時点でコピペしましょう。紛失した場合は再発行してください。  

``` python :LineNotify.py
lineNotifyToken = "LINE NotifyのAPIキーを入れてください"
```

<img src="https://github.com/cryptocat-miner/BitMexLineNotifyBot/blob/master/images/token_generate.png" width="320px" alt="token generate">  
<img src="https://github.com/cryptocat-miner/BitMexLineNotifyBot/blob/master/images/talk_room_select.png" width="320px" alt="talk_room_selecte">  
<img src="https://github.com/cryptocat-miner/BitMexLineNotifyBot/blob/master/images/token_generated.png" width="320px" alt="token generated">  

## BitMexのAPIキー発行・設定
[BitMex](https://www.bitmex.com/) にログインし、API -> APIキーの管理 -> APIキーを作成 画面で任意の名前をつけてAPIキーを作成を押してください。  
CIDRは特に不要、キーのアクセス許可は注文/注文キャンセルどちらでも構いません。出金にはチェックを入れない方が無難です。  
2FAの設定をしている方は2要素トークン欄への入力を忘れないでください。  
<img src="https://github.com/cryptocat-miner/BitMexLineNotifyBot/blob/master/images/bitmex_apikey.png" width="320px" alt="bitmex_apikey">  

作成したAPIキーのをccxtWrapper.pyにコピペします。  
IDをapikey、秘密鍵をsecretにそれぞれ貼り付けてください。  
テストネット/メインネットを切り替えられるようにしていますので、普通に取引する方メインネットの方(elseの方)に間違えずに貼り付けてください。  


``` python :ccxtWrapper.py
def __init__(self, exchangeNetwork: str):
        if exchangeNetwork == "test":
            self.__bitmex = ccxt.bitmex({
                "apiKey": "BitMexテストネットのAPIキーを入れてください",
                "secret": "BitMexテストネットのシークレットキーを入れてください",
            })
            self.__bitmex.urls["api"] = self.__bitmex.urls["test"]
            print("connection:test net")
        else:
            self.__bitmex = ccxt.bitmex({
                "apiKey": "BitMexメインネットのAPIキーを入れてください",
                "secret": "BitMexメインネットのシークレットキーを入れてください",
            })
            print("connection:main net")
```


## 監視bot起動
BitMexとLINE NotifyのAPIキーをコードにコピペしたらbotを起動します。  
LineNotifyBot.pyでテストネット/メインネットを切り替えるコードで以下のようにメインネットが選択されている事を確認してください。  

``` python :LineNotifyBot.py
# メインプログラム
# 初期化
# bitmex = ccxtWrapper.ccxtWrapper(ccxtWrapper.ccxtWrapper.EXCHANGE_TYPE_TESTNET) #テストネット
bitmex = ccxtWrapper.ccxtWrapper(ccxtWrapper.ccxtWrapper.EXCHANGE_TYPE_MAINNET)
```
LineNotifyBot.py を開き、その状態でCloud9画面上部真ん中のRunボタンを押すとbotが起動します。  
<img src="https://github.com/cryptocat-miner/BitMexLineNotifyBot/blob/master/images/run.png" width="320px" alt="run">  

自分のLINEにbot起動通知が来ているか確認してください。

<img src="https://github.com/cryptocat-miner/BitMexLineNotifyBot/blob/master/images/line_notify_1.jpg" width="320px" alt="LINE通知1">  

## 使用ライブラリ
ccxt (MIT License)  
Copyright © 2017 Igor Kroitor  
https://github.com/ccxt/ccxt  
