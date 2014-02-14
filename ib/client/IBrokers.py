# from dateutil import parser

# from ib.ext.Order import Order
# from pandas.lib import Timestamp

import numpy as np
from time import sleep
import uuid

from ib.ext.Contract import Contract
from ib.ext.ExecutionFilter import ExecutionFilter

from ib.client.Portfolio import AccountPacket, PortfolioPacket
from ib.ext.EClientSocket import EClientSocket
from ib.client.sync_wrapper import SyncWrapper

allMethods = []
def ref(method):
    allMethods.append(method.__name__)
    return method


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
        self.ref_nums = []
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
            self.client_id = np.random.randint(0,1000)

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
            if ref_id not in self.ref_nums:
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
        if self.account.child_accounts != []:
            return self.account.child_accounts
        else:
            sleep(1)
            return self.connection.reqManagedAccts()

    def get_contract(self, contract):
        ref = self.request_reference_id(integer=True)
        self.connection.reqContractDetails(ref, contract)
        sleep(1)
        return ref

    def get_executions(self, filter_):
        ref = self.request_reference_id(integer=True)
        self.connection.reqExecutions(ref, filter_)


    @ref
    def disconnect(self):
        self.connection.eDisconnect()


con = Contract()
con.m_localSymbol = 'HEZ4'
con.m_secType = 'FUT'
#con.m_currency = 'USD'
con.m_exchange = 'GLOBEX'

filter = ExecutionFilter()
filter.m_symbol = 'ES'

client = IBClient(call_msg=True)
client.get_executions(filter)
sleep(2)
client.disconnect()

