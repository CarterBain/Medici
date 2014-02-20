# from dateutil import parser


# from pandas.lib import Timestamp

import numpy as np
from time import sleep
import uuid

from ib.ext.Contract import Contract
from ib.ext.Order import Order

from ib.client.Portfolio import AccountPacket, PortfolioPacket
from ib.ext.EClientSocket import EClientSocket
from ib.client.sync_wrapper import SyncWrapper

#Todo: Deprecate
# allMethods = []
# def ref(method):
#     allMethods.append(method.__name__)
#     return method


class IBClient(object):
    fields = {'trades': 'TRADES',
              'midpoint': 'MIDPOINT',
              'bid': 'BID',
              'ask':'ASK',
              'bid_ask':'BID_ASK',
              'hist_vol': 'HISTORICAL_VOLATILITY',
              'imp_vol': 'OPTION_IMPLIED_VOLATILITY'}

    def __init__(self, sync=True, name=None, call_msg=True, host=None, port=None, client_id=None):
        self.name = name
        self.host = host
        self.port = port
        self.client_id = client_id
        self.ref_nums = [0]
        self.wrapper = SyncWrapper()
        self.connection = EClientSocket(self.wrapper)
        self.account = self.wrapper.account
        self.contracts = self.wrapper.contracts

        if self.host is None:
            self.host = 'localhost'
        if self.port is None:
            self.port = 7496
        if call_msg is False:
            self.wrapper.suppress = True
        if self.client_id is None:
            self.client_id = 0

        # listen to execution
        self.wrapper.register(self.method, events='execution')
        self.__connect__ = self.connection.eConnect(self.host, self.port, self.client_id)
        sleep(.2)

    def request_reference_id(self, integer=False):
        if not integer:
            ref_id = uuid.uuid4().hex
            if ref_id in self.ref_nums:
                return self.request_reference()
            else:
                self.ref_nums.append(ref_id)
                return ref_id
        else:
            ref_id = '{0:09d}'.format(np.random.randint(0,999999999))
            if ref_id >  max(self.ref_nums):
                return int(ref_id)
            else:
                return self.request_reference(integer=True)

    def method(self, sender, event, msg=None):
        print "[{0}] got event {1} with message {2}".format(self.name, event, msg)

    def __flatten__(self, container):
        for i in container:
            if isinstance(i, list) or isinstance(i, tuple):
                for j in self.__flatten__(i):
                    yield j
            else:
                yield i

    def account_updates(self, acct):
        #get a unique id
        reference = self.request_reference_id()

        #append a new packet container to account
        self.account.append_request(reference, AccountPacket(acct), PortfolioPacket(acct))
        self.wrapper.ref_id = reference
        self.connection.reqAccountUpdates(1, acct)
        sleep(1)
        return reference

    def managed_accounts(self):
        self.connection.reqManagedAccts()
        sleep(.2)
        if not self.account.child_accounts:
            return self.account.child_accounts
        else:
            sleep(1)
            return self.connection.reqManagedAccts()

    def get_contract(self, contract):
        ref = self.request_reference_id(integer=True)
        self.connection.reqContractDetails(ref, contract)
        sleep(1)
        return ref

    #Todo: This is currently showing weird behavior
    def get_executions(self, filter_):
        ref = self.request_reference_id(integer=True)
        self.connection.reqExecutions(ref, filter_)

    #Todo: IB isn't sending anything back is this normal?
    def place_order(self, contract, order, id_=None):
        if not id_:
            ref = self.request_reference_id(integer=True)
        else:
            ref = id_
        self.connection.placeOrder(ref, contract, order)

        return ref

    def get_all_open_orders(self):
        #Todo: need class structure to hold requests
        ref = self.request_reference_id()
        self.connection.reqAllOpenOrders()
        return ref

    def get_auto_open_orders(self, boolean):
        #Todo a single order returns order details numerous times
        self.connection.reqAutoOpenOrders(boolean)

    def request_fundamental_data(self, contract, report):
        types = ['Estimates', 'Summary', 'Financial Statements']
        if report not in types:
            raise Exception('invalid request for report')
        ref = self.request_reference_id(integer=True)
        self.connection.reqFundamentalData(ref, contract, report)

    def global_cancel(self):
        #Todo: output the orders effected
        self.connection.reqGlobalCancel()

    def historical_data(self, contract, endDateTime, durationStr, barSizeSetting, whatToShow, useRTH, formatDate):
        ref = self.request_reference_id()
        self.connection.reqHistoricalData(ref,
                                          contract,
                                          endDateTime,
                                          durationStr,
                                          barSizeSetting,
                                          whatToShow,
                                          useRTH,
                                          formatDate)



    def disconnect(self):
        self.connection.eDisconnect()


con = Contract()
con.m_localSymbol = 'GOOG'
con.m_secType = 'STK'
#con.m_currency = 'USD'
con.m_exchange = 'SMART'

order = Order()
order.m_action = 'BUY'
order.m_totalQuantity = 2
order.m_tif = 'GTC'
order.m_orderType = 'MKT'
order.m_faGroup = 'ALL'
order.m_faMethod = 'AvailableEquity'

client = IBClient()
client.global_cancel()
sleep(4)

client.disconnect()

