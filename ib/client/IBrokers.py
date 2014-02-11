import numpy as np
from time import sleep
from dateutil import parser
from ib.ext.Contract import Contract
from ib.ext.Order import Order
from pandas.lib import Timestamp
from ib.ext.EClientSocket import EClientSocket
from ib.client.sync_wrapper import SyncWrapper

allMethods = []
def ref(method):
    allMethods.append(method.__name__)
    return method

#Todo: add asynchronous routines
class IBClient(object):
    fields = {'trades': 'TRADES',
              'midpoint': 'MIDPOINT',
              'bid': 'BID',
              'ask':'ASK',
              'bid_ask':'BID_ASK',
              'hist_vol': 'HISTORICAL_VOLATILITY',
              'imp_vol': 'OPTION_IMPLIED_VOLATILITY'}
    return_msg = None

    def __init__(self, sync=True, name=None, call_msg=True, host=None, port=None, clientId=None):
        self.sync = sync
        self.name = name
        self.host = host
        self.port = port
        self.clientId = None
        self.wrapper = SyncWrapper()
        self.connection = EClientSocket(self.wrapper)

        if self.host is None:
            self.host = 'localhost'
        if self.port is None:
            self.port = 7496
        if call_msg is False:
            self.wrapper.suppress = True
        if self.clientId is None:
            self.clientId = np.random.randint(0,1000)

        # listen to execution
        self.wrapper.register(self.method, events='execution')
        self.__connect__ = self.connection.eConnect(self.host, self.port, self.clientId)

    def method(self, sender, event, msg=None):
        print "[{0}] got event {1} with message {2}".format(self.name, event, msg)

    def __hold_for_request__(self):
        while self.wrapper.handler is None:
            sleep(.001)

    def __flatten__(self, container):
        for i in container:
            if isinstance(i, list) or isinstance(i, tuple):
                for j in self.__flatten__(i):
                    yield j
            else:
                yield i

    def list_accounts(self):
        self.wrapper.emitter = ['managedAccounts']
        self.caller = self.wrapper.handler = None
        self.return_msg = self.wrapper.return_list = []
        client.connection.reqManagedAccts()
        self.__hold_for_request__()
        self.caller = self.wrapper.handler
        while self.caller is self.wrapper.handler:
            if self.return_msg == self.wrapper.return_list:
                break
            self.return_msg = self.wrapper.return_list
            sleep(.001)
        self.wrapper.emitter = []
        if not self.wrapper.return_list:
            return 'Request failed'
        return list(self.__flatten__(dict_.values() for dict_ in self.wrapper.return_list))

    def tws_connection_time(self):
        local = parser.parse(self.connection.TwsConnectionTime())
        return Timestamp(local).tz_convert('UTC')

    #Todo: finish implied volatility calculation
    # def calculate_implied_volatility(self, contract, option_price, underlying_price, reqId = None):
    #     self.caller = self.wrapper.handler = client.return_msg = None
    #     if reqId is None:
    #         reqId = np.random.randint(0,1000)
    #     self.connection.calculateImpliedVolatility(reqId, contract, option_price, underlying_price)
    #Todo: finish option price calculation (err: Requested market data is not subscribed)
    # def calculate_option_price(self, contract, volatility, underlying_price, reqId=None):
    #     self.caller = self.wrapper.handler = client.return_msg = None
    #     if reqId is None:
    #         reqId = np.random.randint(0,1000)
    #     self.connection.calculateOptionPrice(reqId, contract, volatility, underlying_price)
    #Todo: Another options function that needs implemented
    # def exercise_options(self):
    #     self.connection.exerciseOptions

        # self.connection.cancelCalculateImpliedVolatility
        # self.connection.cancelCalculateOptionPrice
        # self.connection.cancelFundamentalData
        # self.connection.cancelHistoricalData
        # self.connection.cancelMktData
        # self.connection.cancelMktDepth
        # self.connection.cancelNewsBulletins
        # self.connection.cancelOrder
        # self.connection.cancelRealTimeBars
        # self.connection.cancelScannerSubscription

    def check_connected(self):
        self.wrapper.emitter = ['error']
        self.caller = self.wrapper.handler = None
        self.return_msg = self.wrapper.return_list = []
        self.connection.checkConnected(self.host)
        self.__hold_for_request__()
        self.caller = self.wrapper.handler
        while self.caller is self.wrapper.handler:
            if self.return_msg == self.wrapper.return_list:
                break
            self.return_msg = self.wrapper.return_list
            sleep(.001)
        self.wrapper.emitter = []
        if not self.wrapper.return_list:
            return 'Request failed'
        msg = [x['errorMsg'] for x in self.wrapper.return_list]
        return msg[0] if len(msg) == 1 else msg

    def connect(self):
        check_connection = self.check_connected()
        if check_connection == 'Already connected.':
            return check_connection
        self.connection.eConnect(self.host, self.port, self.clientId)
        return 'Connecting...'

    def is_connected(self):
        return self.connection.isConnected()

    def place_order(self, contract, order, id_=None):
        if id_ is None:
            id_ = np.random.randint(0,10000000)
        self.wrapper.emitter = ['openOrder', 'orderStatus']
        self.caller = self.wrapper.handler = None
        self.return_msg = self.wrapper.return_list = []
        self.connection.placeOrder(id_,contract, order)
        self.__hold_for_request__()
        self.caller = self.wrapper.handler
        while self.caller is self.wrapper.handler:
            if self.return_msg == self.wrapper.return_list:
                break
            self.return_msg = self.wrapper.return_list
            sleep(.001)
        self.wrapper.emitter = []
        if not self.wrapper.return_list:
            return 'Request failed'
        msg = list(self.__flatten__(x.items() for x in self.wrapper.return_list))
        #Todo: what happens here with multiple orders
        return dict(zip(msg[::2], msg[1::2]))

        # self.connection.reader


    # def update_account(self, acct):
    #     self.caller = self.wrapper.handler = client.return_msg = None
    #     self.connection.reqAccountUpdates(subscribe = True, acctCode=acct)
    #     self.__hold_for_request__()
    #     self.caller = self.wrapper.handler
    #     while self.caller is self.wrapper.handler:
    #         if client.return_msg == client.wrapper.accountName, client.wrapper.key:
    #             break
    #         client.return_msg = client.wrapper.accountsList
    #         sleep(.001)

    def request_fa(self, data_request):
        map = {'groups': 1,
               'profiles' : 2,
               'account aliases': 3}
        self.connection.requestFA(map[data_request])

        # self.connection.replaceFA
        # self.connection.reqAllOpenOrders
        # self.connection.reqAutoOpenOrders
        # self.connection.reqContractDetails
        # self.connection.reqCurrentTime
        # self.connection.reqExecutions
        # self.connection.reqFundamentalData
        # self.connection.reqGlobalCancel
        # self.connection.reqHistoricalData
        # self.connection.reqIds
        # self.connection.reqManagedAccts
        # self.connection.reqMarketDataType
        # self.connection.reqMktData
        # self.connection.reqMktDepth
        # self.connection.reqNewsBulletins
        # self.connection.reqOpenOrders
        # self.connection.reqRealTimeBars
        # self.connection.reqScannerParameters
        # self.connection.reqScannerSubscription
        # self.connection.send
        # self.connection.sendEOL
        # self.connection.sendMax
        # self.connection.sendMax_0
        # self.connection.send_0
        # self.connection.send_1
        # self.connection.send_2
        # self.connection.send_3
        # self.connection.send_4
        # self.connection.serverVersion
        # self.connection.setServerLogLevel
        # self.connection.wrapper

    @ref
    def disconnect(self):
        self.connection.eDisconnect()


con = Contract()
con.m_symbol = 'AAPL'
con.m_secType = 'OPT'
con.m_currency = 'USD'
con.m_strike = 305
con.m_right = 'PUT'
con.m_exchange = 'SMART'
con.m_expiry = "20140516"

ord = Order()
ord.m_action = 'BUY'
ord.m_tif = 'GTC'
ord.m_transmit = True
ord.m_totalQuantity = 1
ord.m_orderType = 'MKT'
ord.m_faGroup = 'All'
ord.m_faMethod = 'AvailableEquity'
## ord.m_faPercentage = '100'

#Todo: OrderStatus contains margin data, and strange commission values
client = IBClient()#call_msg=False)

client.request_fa('groups')
sleep(3)
client.disconnect()


