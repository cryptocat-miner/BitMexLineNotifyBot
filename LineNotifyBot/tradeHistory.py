import ccxtWrapper
import LineNotify
import io


class tradeHistory(ccxtWrapper.ccxtWrapper):

    exchange = None
    tradeHistory = None
    latestTradeHistory = None
    tradeHistoryList = list()

    def __init__(self, instance:ccxtWrapper.ccxtWrapper):
        self.exchange = instance
        self.tradeHistory = self.exchange.fetchMyTrades(since=None,limit=None)

    def checkTradeHistory(self):
        tradeHistory = self.exchange.fetchMyTrades(since=None, limit=None)

        if tradeHistory != None:
            if self.latestTradeHistory != None:
                if self.latestTradeHistory != tradeHistory[0]:
                    tradeHistoryItem = self.tradeHistoryItem()
                    for trade in tradeHistory:
                        print(trade)
                        print("\r\n\r\n")
                        if trade["id"] == self.latestTradeHistory["id"]:
                            if tradeHistoryItem.amount != 0:
                                tradeHistoryItem.averagePrice = tradeHistoryItem.averagePrice / tradeHistoryItem.amount
                            self.tradeHistoryList.append(tradeHistoryItem)
                            break
                        if tradeHistoryItem.orderId == trade["info"]["orderID"]:
                            tradeHistoryItem.amount += trade["amount"]
                            tradeHistoryItem.averagePrice = tradeHistoryItem.averagePrice + (trade["info"]["lastPx"] * trade["amount"])
                            tradeHistoryItem.feeCost += trade["fee"]["cost"]
                        else:
                            if tradeHistoryItem.orderId != None:
                                if tradeHistoryItem.amount != 0:
                                    tradeHistoryItem.averagePrice = tradeHistoryItem.averagePrice / tradeHistoryItem.amount
                                self.tradeHistoryList.append(tradeHistoryItem)
                                tradeHistoryItem = self.tradeHistoryItem()
                            tradeHistoryItem.execType = trade["info"]["execType"]
                            tradeHistoryItem.orderId = trade["info"]["orderID"]
                            tradeHistoryItem.text = trade["info"]["text"]
                            tradeHistoryItem.amount = trade["amount"]
                            if tradeHistoryItem.text != "Liquidation":
                                tradeHistoryItem.averagePrice = trade["info"]["lastPx"] * trade["amount"]
                            else:
                                tradeHistoryItem.averagePrice = trade["info"]["stopPx"] * trade["amount"]
                            tradeHistoryItem.feeCost = trade["fee"]["cost"]
                            tradeHistoryItem.feeRate = trade["fee"]["rate"]
                            tradeHistoryItem.side = trade["side"]
                            tradeHistoryItem.orderType = trade["type"]
                            
                            
                    for trade in self.tradeHistoryList:
                        if trade.execType == "Trade":
                            self.sendTradeMessage(amount=trade.amount, price=trade.averagePrice, feeCost=trade.feeCost, side=trade.side, orderType=trade.orderType, text=trade.text)
                        elif trade.execType == "Funding":
                            self.sendFundingMessage(amount=trade.amount, price=trade.averagePrice, feeCost=trade.feeCost, feeRate=trade.feeRate)

            self.tradeHistory = tradeHistory
            self.latestTradeHistory = self.tradeHistory[0]
            self.tradeHistoryList.clear()

    def sendTradeMessage(self, amount:int, price:float, feeCost:float, side:str, orderType:str, text:str):
        message = "取引情報を通知します\r\n"
        if side == "buy":
            message += "方向:ロング\r\n"
        elif side == "sell":
            message += "方向:ショート\r\n"
        if orderType == "limit":
            message += "タイプ:指値\r\n"
        elif orderType == "market":
            message += "タイプ:成行\r\n"
        elif orderType == "stop":
            message += "タイプ:ストップ成行\r\n"
        elif orderType == "stoplimit" and text == "Liquidation":
            message += "タイプ:精算\r\n"
        elif orderType == "marketiftouched":
            message += "タイプ:利食い成行\r\n"
        elif orderType == "limitiftouched":
            message += "タイプ:利食い指値\r\n"
        else:
            message += "タイプ:不明\r\n"
        message += "取引量:" + str(int(amount)) + "\r\n"
        message += "価格:" + "{:.1f}".format(price) + "\r\n"
        if (feeCost >= 0):
            message += "取引手数料:-" + "{:.4f}".format(abs(feeCost)) + " XBT"
        else:
            message += "取引手数料:+" + "{:.4f}".format(abs(feeCost)) + " XBT"

        LineNotify.PostMessage(message)

    def sendFundingMessage(self, amount:int, price:float, feeCost:float, feeRate:float):
        message = "Funding情報を通知します\r\n"
        message += "数量:" + str(amount) + "\r\n"
        message += "執行価格:" + "{:.1f}".format(price) + "\r\n"
        if (feeCost >= 0):
            message += "Funding手数料:-" + "{:.4f}".format(abs(feeCost)) + " XBT(" + "{:.4f}".format(feeRate * 100) + "%)"
        else:
            message += "Funding手数料:+" + "{:.4f}".format(abs(feeCost)) + " XBT(" + "{:.4f}".format(feeRate * 100) + "%)"

        LineNotify.PostMessage(message)


    class tradeHistoryItem:
        execType = None
        orderType = None
        orderId = None
        text = None
        id = None
        side = None
        takerOrMaker = None
        amount = 0.0
        averagePrice = 0.0
        feeCost = 0.0
        feeRate = 0.0
