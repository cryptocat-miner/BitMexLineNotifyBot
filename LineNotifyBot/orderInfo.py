

def getOrderText(info):
    message = ""
    cr = "\r\n"
    try:
        price = "価格:" + str(info["price"]) + cr
        amount = "数量:" + str(info["amount"]) + cr
        side = "ポジション:"
        type = "タイプ:"

        if info["side"] == "sell":
            side = side + "ショート(売り)" + cr
        else:
            side = side + "ロング(買い)" + cr
        if info["type"] == "market":
            type = type + "成行"
        elif info["type"] == "limit":
            type = type + "指値"
        elif info["type"] == "stop":
            type = type + "ストップ成行"
            price = "トリガ価格:" + str(info["info"]["stopPx"]) + cr
        elif info["type"] == "stopLimit":
            type = type + "ストップ指値"
            price = "トリガ価格:" + str(info["info"]["stopPx"]) + cr + "指値価格:" +str(info["price"]) + cr
        message = price + amount + side + type

    except Exception as error:
        print(error)

    return message

def getBalanceText(balance):
   message = ""
   cr = "\r\n"
   total = "合計資産" + "{:.4f}".format(balance["total"]) + " XBT" + cr
   used = "使用済:" + "{:.4f}".format(balance["used"]) + " XBT" + cr
   free = "使用可能:" + "{:.4f}".format(balance["free"]) + " XBT" + cr
   
   message = total + used + free
    

   return message
