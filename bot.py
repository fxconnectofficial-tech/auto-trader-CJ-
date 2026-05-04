import re
import MetaTrader5 as mt5
from telethon import TelegramClient, events

# 🔑 TELEGRAM API
api_id = 35433634
api_hash = "a9468f9a7654ae557f8eb8ce74b2c79f"

# 🚀 CONNECT MT5
mt5.initialize()

client = TelegramClient('session', api_id, api_hash)

@client.on(events.NewMessage)
async def handler(event):
    text = event.raw_text

    if "SIGNAL ALERT" in text:

        try:
            direction = re.search(r"Signal:\s*(BUY|SELL)", text).group(1)
            symbol = re.search(r"Ticker:\s*(\w+)", text).group(1)

            sl = float(re.search(r"SL:\s*(\d+)", text).group(1))
            tp1 = float(re.search(r"TP1:\s*(\d+)", text).group(1))

            tick = mt5.symbol_info_tick(symbol)

            if direction == "BUY":
                price = tick.ask
                order_type = mt5.ORDER_TYPE_BUY
            else:
                price = tick.bid
                order_type = mt5.ORDER_TYPE_SELL

            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": 0.01,
                "type": order_type,
                "price": price,
                "sl": sl,
                "tp": tp1,
                "deviation": 10,
                "magic": 123456,
                "comment": "Telegram Auto Trade",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }

            result = mt5.order_send(request)
            print("Trade sent:", result)

        except Exception as e:
            print("Error:", e)

client.start()
print("Bot running...")
client.run_until_disconnected()