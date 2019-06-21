import requests
from urllib.parse import urlencode
# from websocket import create_connection
import threading
import websocket

URL_REST = 'http://data-store-testing.bitmart.com'
URL_WS = 'ws://data-store-testing.bitmart.com:80'
version = 'v1'


def _handle_response(response):
    """Internal helper for handling API responses from the Binance server.
    Raises the appropriate exceptions when necessary; otherwise, returns the
    response.
    """
    if not str(response.status_code).startswith('2'):
        raise ValueError('Response error. response:{}, response.text:{}'.format(response, response.text))
    try:
        return response.json()
    except ValueError:
        raise ValueError('Invalid Response:{}'.format(response.text))


def _request(method, url, params=None, data=None):
    if params:
        url = url + '?' + urlencode(params)

    if method == 'get':
        response = requests.get(url)
        return _handle_response(response)

    if method == 'post':
        response = requests.post(url, data=data)
        return _handle_response(response)


def get_history_kline(exchange, symbol, from_t=None, to_t=None, limit=500, interval=1):
    """
        获取交易对历史kline
    Parameters
    ------
        :param exchange: exchange name
        :type exchange: string
        :param symbol: trade pair name
        :type symbol: string
        :param from_t: data from timestamp
        :type from_t: int
        :param to_t: data to timestamp
        :type to_t: int
        :param limit: data length
        :type limit: int
        :param interval: kline interval
        :type interval: int
    return
    -------
      DataFrame
        {
            'status': 'ok',
            'msg': '',
            'data': [
                [1558775162, # timestamp
                0.031530, # open
                0.031535, # high
                0.031282, # low
                0.031282, # close
                104.581400], # volume
                ...
            ]
        }
    """
    params = {
        'exchange': exchange,
        'symbol': symbol,
        'limit': limit,
        'interval': interval}
    if from_t: params['from_t'] = from_t
    if to_t: params['to_t'] = to_t
    url = URL_REST + '/' + version + '/klines'
    return _request('get', url, params)


class Singleton(type):

    def __init__(self, *args, **kwargs):
        self.__instance = None
        super().__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        if self.__instance is None:
            self.__instance = super().__call__(*args, **kwargs)
            return self.__instance
        else:
            return self.__instance

class Socket(metaclass=Singleton):
    def __init__(self):
        self.ws = None

    def _start_user_timer(self, callback):
        self._user_timer = threading.Timer(4, self._recv_msg, (callback,))
        self._user_timer.setDaemon(True)
        self._user_timer.start()

    def _recv_msg(self, callback):
        info = self.ws.recv()
        callback(info)
        self._start_user_timer(callback)

    def ws_run(self, callback):
        print("Collecting updates from quant data server...")
        self.ws = create_connection(URL_WS + '/echo')
        self._start_user_timer(callback)
