
#!/usr/bin/python3
import time
from datetime import datetime
import calendar
import ccxt
import ccxtWrapper
import math
import matplotlib.pyplot as plt
import io

from pyti.exponential_moving_average import exponential_moving_average as ema
from pyti.moving_average_convergence_divergence import moving_average_convergence_divergence as macd
from pyti.relative_strength_index import relative_strength_index as rsi


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
