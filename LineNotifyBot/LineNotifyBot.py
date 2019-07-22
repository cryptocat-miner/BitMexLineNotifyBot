
#!/usr/bin/python3
import time
from datetime import datetime
import calendar
import ccxt
import ccxtWrapper
import math
import io

import numpy
import orderManager

import LineNotify


# ------------------------------------------------------------------------------------------------
# メインプログラム
# 初期化
# bitmex = ccxtWrapper.ccxtWrapper(ccxtWrapper.ccxtWrapper.EXCHANGE_TYPE_TESTNET) #テストネット
bitmex = ccxtWrapper.ccxtWrapper(ccxtWrapper.ccxtWrapper.EXCHANGE_TYPE_MAINNET)
mOrderManager = orderManager.orderManager(bitmex)

openOrders = bitmex.fetchOpenOrders()

while True:
    currentTime = datetime.utcnow()  # 現在時刻(UTC)

    mOrderManager.switchState()
    time.sleep(6)
