# from dateutil import parser
# from ib.ext.Contract import Contract
# from ib.ext.Order import Order
# from pandas.lib import Timestamp

import numpy as np
from time import sleep
import uuid

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

    def request_reference_id(self):
        ref_id = uuid.uuid4().hex
        if ref_id in self.ref_nums:
            return self.request_reference()
        else:
            self.ref_nums.append(ref_id)
            return ref_id

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



    @ref
    def disconnect(self):
        self.connection.eDisconnect()


client = IBClient(call_msg=False)
ref = client.account_updates('DU169492')

print [pck.contract.__dict__ for pck in client.account[ref]['portfolio'].messages]
