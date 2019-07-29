import ccxt
from datetime import datetime
import calendar
import time
import LineNotify


class ccxtWrapper:
    ORDER_TYPE_LIMIT = "limit"  # 指値
    ORDER_TYPE_MARKET = "market"  # 成行
    ORDER_TYPE_STOP_MARKET = "stop"  # ストップ成行
    ORDER_TYPE_STOP_LIMIT = "stopLimit"  # ストップ指値

    PERIOD_1min = "1m"
    PERIOD_5min = "5m"
    PERIOD_1h = "1h"
    PERIOD_1d = "1d"

    EXCHANGE_TYPE_TESTNET = "test"
    EXCHANGE_TYPE_MAINNET = "main"

    ORDER_SIDE_BUY = "buy"  # 買い注文
    ORDER_SIDE_SELL = "sell"  # 売り注文

    # bitmex用のオブジェクト生成・取得
    # def createBitmex(exchangeNetwork:str):
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

    # 現在価格取得
    def fetchTicker(self):
        ticker = None
        symbol = "BTC/USD"
        print("fetchTicker()")
        try:
            ticker = self.__bitmex.fetch_ticker(symbol)
        except Exception as error:
            print(error)
            if str(error).find("HTTPSConnectionPool") == -1:
                #LineNotify.PostMessage("エラー発生\r\n" + "メソッド:fetchTicker()\r\n" + "エラー内容:\r\n" + str(error) + "\r\n")
                ticker = None

        return ticker

    # 資産取得
    def fetchBalance(self):
        balance = None
        print("fetchBalance()")
        try:
            balance = self.__bitmex.fetch_balance()
            balance = balance["BTC"]
        except Exception as error:
            print(error)
            if str(error).find("HTTPSConnectionPool") == -1:
                #LineNotify.PostMessage("エラー発生\r\n" + "メソッド:fetchBalance()\r\n" + "エラー内容:\r\n" + str(error) + "\r\n")
                balance = None

        return balance
    
    def fetchMyTrades(self, since, limit):
        trades = None
        symbol = "BTC/USD"
        print("fetchTarde()")
        try:
            #"reverse":Trueで新しい順に配列の最後から詰められる
            trades = self.__bitmex.fetch_my_trades(symbol, since=since, limit=limit, params={"reverse": True})
            #listの"datetime"をキーにreverseする事で配列の最初(index=0)からソートする
            trades.sort(key=lambda x: x["datetime"],reverse=True)
        except Exception as error:
            print(error)
            trades = None
        return trades

    # 注文
    def Order(self, type: str, side: str, amount: float, price: float, params: dict):
        order = None  # 初期値
        symbol = "BTC/USD"
        print("Order()")
        try:
            if type == self.ORDER_TYPE_LIMIT:
                order = self.__bitmex.create_order(symbol, type, side, amount, price, params)
            elif type == self.ORDER_TYPE_MARKET:
                order = self.__bitmex.create_order(symbol, type, side, amount, None)
            elif type == self.ORDER_TYPE_STOP_MARKET:
                order = self.__bitmex.create_order(symbol, type, side, amount, None, params)
            elif type == self.ORDER_TYPE_STOP_LIMIT:
                order = self.__bitmex.create_order(symbol, type, side, amount, price, params)

            # for orderSingle in order:
            #    print(str(orderSingle) + ":" + str(order[str(orderSingle)]))
        except Exception as error:
            print(error)  # 異常時はエラーメッセージを表示する
            if str(error).find("HTTPSConnectionPool") == -1:
                #LineNotify.PostMessage("エラー発生\r\n" + "メソッド:Order()\r\n" + "エラー内容:\r\n" + str(error) + "\r\n")
                order = None

        return order

    # 注文キャンセル
    def cancelOrder(self, orderId: str):
        cancel = None
        print("cancelOrder()")
        try:
            cancel = self.__bitmex.cancel_order(orderId)
            # print(cancel)
        except Exception as error:
            print(error)
            if str(error).find("HTTPSConnectionPool") == -1:
                #LineNotify.PostMessage("エラー発生\r\n" + "メソッド:cancelOrder()\r\n" + "エラー内容:\r\n" + str(error) + "\r\n")
                cancel = None

        return cancel

    # 現在の注文情報を取得
    def fetchOpenOrders(self):
        openOrders = None
        print("fetchOpenOrders()")
        try:
            openOrders = self.__bitmex.fetch_open_orders()
            # print(openOrders)
            # if len(openOrders) == 0:
            #    openOrders = None
        except Exception as error:
            print(error)
            if str(error).find("HTTPSConnectionPool") == -1:
                #LineNotify.PostMessage("エラー発生\r\n" + "メソッド:fetchOpenOrders()\r\n" + "エラー内容:\r\n" + str(error) + "\r\n")
                openOrders = None

        return openOrders

    # 現在のポジション情報を取得
    def privateGetPosition(self):
        position = None
        print("privateGetPosition()")
        try:
            position = self.__bitmex.private_get_position()
            # print(position)
        except Exception as error:
            print(error)
            if str(error).find("HTTPSConnectionPool") == -1:
                #LineNotify.PostMessage("エラー発生\r\n" + "メソッド:privateGetPosition()\r\n" + "エラー内容:\r\n" + str(error) + "\r\n")
                position = None

        return position

    # レバレッジ設定
    def privatePostPositionLeverage(self, leverage: int):
        print("privatePostPositionLeverage()")
        try:
            self.__bitmex.private_post_position_leverage({"symbol": "XBTUSD", "leverage": str(leverage)})
        except Exception as error:
            print(error)
            # if str(error).find("HTTPSConnectionPool") == -1:
            #LineNotify.PostMessage("エラー発生\r\n" + "メソッド:privatePostPositionLeverage()\r\n" + "エラー内容:\r\n" + str(error) + "\r\n")

    #過去のローソク足取得(period=足の期間(単位), since=取得し始める時間[min])
    def fetchOhlcv(self, period: str, since: int):
        ohlcv = None
        print("fetchOhlcv()")
        try:
            now = datetime.utcnow()  # 現在時刻(UTC)
            unixTime = calendar.timegm(now.utctimetuple())  # Unix時間に変換
            since = (unixTime - 60 * since) * 1000  # 10分前のUnix時間算出→ms単位に変換

            ohlcv = self.__bitmex.fetch_ohlcv("BTC/USD", period, since, limit=500)
        except Exception as error:
            print(error)
            if str(error).find("HTTPSConnectionPool") == -1:
                #LineNotify.PostMessage("エラー発生\r\n" + "メソッド:fetchOhlcv()\r\n" + "エラー内容:\r\n" + str(error) + "\r\n")
                ohlcv = None

        return ohlcv
