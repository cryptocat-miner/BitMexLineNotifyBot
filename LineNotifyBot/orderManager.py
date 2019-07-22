import ccxt
from datetime import datetime
from datetime import timedelta
import calendar
import time
from enum import Enum
import ccxtWrapper
import math
import LineNotify
import orderInfo


class orderManagementEnum(Enum):
    NO_POSITION = 0
    HAVE_POSITION = 1


class orderManager(ccxtWrapper.ccxtWrapper):

    orderManagementState = orderManagementEnum(0)
    exchangeInstance = None
    orderErrorCounter = 0

    isPosition = False
    balance = None
    orderAmount = 0
    positionAmount = 0
    size = 0
    preSize = 0
    btcAmount = 0
    averagePrice = 0
    liquidationPrice = 0  # 清算価格
    maintMargin = 0
    realisedPnl = 0  # 実現損益
    unrealisedPnl = 0  # 未実現損益
    unrealisedRoePcnt = 0  # 未実現損益(ROE%)

    orderCounter = 0

    orederCancelTime = datetime.utcnow()

    totalBlance = 0
    diffBalance = 0

    def __init__(self, instance: ccxtWrapper.ccxtWrapper):
        self.orderManagementState = orderManagementEnum.NO_POSITION
        self.exchangeInstance = instance
        self.changeToNoPositionState()
        self.setPositionDirection()

    def setPositionDirection(self):
        positions = self.exchangeInstance.privateGetPosition()
        if positions != None and len(positions) > 0:
            if positions[0]["currentQty"] != None:
                self.preSize = self.size
                self.size = positions[0]["currentQty"]
            if positions[0]["homeNotional"] != None:
                self.btcAmount = abs(positions[0]["homeNotional"])
            if positions[0]["avgCostPrice"] != None:
                self.averagePrice = round(positions[0]["avgCostPrice"], 2)
            if positions[0]["liquidationPrice"] != None:
                self.liquidationPrice = positions[0]["liquidationPrice"]
            if positions[0]["maintMargin"] != None:
                self.maintMargin = round(
                    positions[0]["maintMargin"] / 100000000, 4)
            if positions[0]["realisedPnl"] != None and positions[0]["rebalancedPnl"] != None:
                self.realisedPnl = round(
                    (positions[0]["realisedPnl"] + positions[0]["rebalancedPnl"]) / 100000000, 4)
            if positions[0]["unrealisedPnl"] != None:
                self.unrealisedPnl = round(
                    positions[0]["unrealisedPnl"] / 100000000, 4)
            if positions[0]["unrealisedRoePcnt"] != None:
                self.unrealisedRoePcnt = round(
                    positions[0]["unrealisedRoePcnt"] * 100, 2)

        balance = self.exchangeInstance.fetchBalance()
        if balance != None:
            # 起動時の一回目に資産情報を通知
            if self.balance == None:
                LineNotify.PostMessage("監視botを起動しました\r\n資産は" + str(round(
                    balance["total"], 4)) + "XBTです")

            self.balance = balance

        if self.balance != None and self.isPosition == False:
            self.totalBlance = self.balance["total"]  # イン-アウトの損益計算用に記憶

        usdPosition = None
        if positions != None:
            for position in positions:
                if position["symbol"] == "XBTUSD":
                    usdPosition = position

            if usdPosition == None or usdPosition["currentQty"] == 0:
                self.isPosition = False
                self.positionAmount = 0
            else:
                self.isPosition = True

                self.positionAmount = abs(usdPosition["currentQty"])
        # else:
        # エラーの場合は前回値を残しておいた方が良いかも？
        #    self.isPosition = False
        #    self.positionAmount = 0

    def switchState(self):
        print("現在の発注管理状態:" + str(self.orderManagementState))
        self.setPositionDirection()
        # 状態毎に処理する関数を分岐
        if self.orderManagementState == orderManagementEnum.NO_POSITION:
            self.noPositionState()
        elif self.orderManagementState == orderManagementEnum.HAVE_POSITION:
            self.havePositionState()
        else:
            print(str(self.orderManagementState) + ":定義されていない状態です")
            print("強制的に初期化します")
            self.changeToNoPositionState()

    def noPositionState(self):
        ret = None

        if self.isPosition == True:
            self.orederCancelTime = datetime.utcnow() + timedelta(hours=1)
            self.changeToHavePositionState()
            self.sendPositionMessage("ポジションを持ちました\r\n")

        return ret

    def havePositionState(self):
        if self.isPosition == False:
            balance = self.exchangeInstance.fetchBalance()
            if balance != None:
                self.diffBalance = balance["total"] - self.totalBlance
                self.totalBalance = balance["total"]
                LineNotify.PostMessage("ポジションを決済しました\r\n今回の取引結果は" + str(round(self.diffBalance, 4)) + "XBTです\r\n現在の合計資産は" + str(
                    round(self.totalBalance, 4)) + "XBTです")
                self.changeToNoPositionState()
            else:
                LineNotify.PostMessage(
                    "ポジションを決済しました\r\nエラーが発生して資産情報は読めませんでした\r\n再度資産情報を読みます")
        else:
            if self.size != self.preSize:
                self.sendPositionMessage("ポジションが変更されました\r\n")

        return None

    def sendPositionMessage(self, message: str):
        balanceMessage = message
        # 資産情報を通知
        balanceMessage = balanceMessage + \
            orderInfo.getBalanceText(self.balance) + "\r\n"
        balanceMessage = balanceMessage + "サイズ:" + str(self.size) + "\r\n"
        balanceMessage = balanceMessage + "値:" + \
            str(self.btcAmount) + " XBT\r\n"
        balanceMessage = balanceMessage + "参入価格:" + \
            str(self.averagePrice) + "\r\n"
        balanceMessage = balanceMessage + "清算価格:" + \
            str(self.liquidationPrice) + "\r\n"
        balanceMessage = balanceMessage + "証拠金:" + \
            str(self.maintMargin) + " XBT\r\n"
        balanceMessage = balanceMessage + \
            "未実現損益(ROE%):" + str(self.unrealisedPnl) + \
            " XBT (" + str(self.unrealisedRoePcnt) + "%)\r\n"
        balanceMessage = balanceMessage + "実現損益:" + \
            str(self.realisedPnl) + " XBT\r\n"
        LineNotify.PostMessage(balanceMessage)

    def changeToNoPositionState(self):
        self.orderCounter = 0
        self.orderErrorCounter = 0
        self.orderManagementState = orderManagementEnum.NO_POSITION
        print("発注管理状態変更:" + str(self.orderManagementState))

    def changeToHavePositionState(self):
        self.orderErrorCounter = 0
        self.orderManagementState = orderManagementEnum.HAVE_POSITION
        print("発注管理状態変更:" + str(self.orderManagementState))
