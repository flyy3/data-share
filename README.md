# DataShare

## Description
Use data of Bitmart, Binance, Huobi and Okcoin to service data analysis.
* Basic market data.
* Basic data processing.
* Advanced data analysis.

## Quite Start

### websocket
```
from data_share import get_history_kline, subscribe
import time
import multiprocessing


def callback(msg):
    print("ws receive:", msg.decode())

def websocket(exchange, symbol):
    topicfilter = ''
    subscribe(topicfilter, callback)
    while True:
        time.sleep(1)

if __name__ == '__main__':

    exchange = 'binance'
    symbol = 'BTC_USDT'

    # websocket get real data
    p = multiprocessing.Process(target = websocket, args = (exchange, symbol,))
    p.start()

```

### rest

```
from data_share import get_history_kline

if __name__ == '__main__':

    exchange = 'binance'
    symbol = 'BTC_USDT'

    # rest get history data
    limit = 10
    data = get_history_kline(exchange, symbol, limit=limit)
    print("rest fetch success:", data)

```