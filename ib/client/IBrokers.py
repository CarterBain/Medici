# from dateutil import parser


# from pandas.lib import Timestamp

from time import sleep
import uuid

import numpy as np

from ib.client.Portfolio import AccountPacket, PortfolioPacket
from ib.ext.ExecutionFilter import ExecutionFilter
from ib.ext.EClientSocket import EClientSocket
from ib.client.sync_wrapper import SyncWrapper


class IBClient(object):
    fields = {'trades': 'TRADES',
              'midpoint': 'MIDPOINT',
              'bid': 'BID',
              'ask': 'ASK',
              'bid_ask': 'BID_ASK',
              'hist_vol': 'HISTORICAL_VOLATILITY',
              'imp_vol': 'OPTION_IMPLIED_VOLATILITY'}

    def __init__(self, name=None, call_msg=True, host=None, port=None, client_id=None):
        self.name = name
        self.host = host
        self.port = port
        self.client_id = client_id
        self.ref_nums = [0]
        self.wrapper = SyncWrapper()
        self.connection = EClientSocket(self.wrapper)
        self.account = self.wrapper.account
        self.contracts = self.wrapper.contracts
        self.executions_ = self.wrapper.executions
        self.order_messages = self.wrapper.order_messages

        if self.host is None:
            self.host = 'localhost'
        if self.port is None:
            self.port = 7496
        if call_msg is False:
            self.wrapper.suppress = True
        if self.client_id is None:
            self.client_id = 0

        # listen to execution
        #self.wrapper.register(self.method, events='execution')
        self.__connect__ = self.connection.eConnect(self.host, self.port, self.client_id)
        self.__gen_order_id__(1)
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
            ref_id = '{0:09d}'.format(np.random.randint(0, 999999999))
            if ref_id > max([x for x in self.ref_nums if type(x) is int]):
                return int(ref_id)
            else:
                return self.request_reference(integer=True)

    def __gen_order_id__(self, num):
        self.connection.reqIds(num)
        return self.wrapper.order_id


    def method(self, sender, event, msg=None):
        print "[{0}] got event {1} with message {2}".format(self.name, event, msg)

    def __track_orders__(self):
        self.connection.reqAutoOpenOrders(1)

    def managed_accounts(self):
        if self.account.child_accounts:
            return self.account.child_accounts
        else:
            self.connection.reqManagedAccts()
            sleep(1)
            if self.account.child_accounts:
                return self.account.child_accounts
            return ['REQUEST FAILED']

    def account_updates(self, acct):
        #get a unique id
        reference = self.request_reference_id()

        #append a new packet container to account
        self.account.append_request(reference, AccountPacket(acct), PortfolioPacket(acct))
        self.wrapper.ref_id = reference
        self.connection.reqAccountUpdates(1, acct)
        sleep(1)
        return reference

    def place_order(self, contract, order):
        self.wrapper.order_id += 100
        ref = self.wrapper.order_id
        self.connection.placeOrder(ref, contract, order)
        sleep(.2)
        return ref

    def cancel_order(self, id):
        self.connection.cancelOrder(id)

    def get_executions(self, efilter=None):
        if not efilter:
            efilter = ExecutionFilter()
        ref = self.request_reference_id(integer=True)
        self.connection.reqExecutions(reqId=ref, filter=efilter)
        sleep(3)  # Todo: This is a ridiculous bottleneck
        return ref

    def get_contract(self, contract):
        ref = self.request_reference_id(integer=True)
        self.connection.reqContractDetails(ref, contract)
        sleep(1)
        return ref

    def portfolio(self, account):
        ref = self.account_updates(account)
        return self.account[ref]['portfolio'].messages

    def account_details(self, account):
        ref = self.account_updates(account)
        return self.account[ref]['account'].messages

    def executions(self, efilter=None):
        ref = self.get_executions(efilter)
        return self.executions_[ref]

    def order_status(self, order_id):
        sleep(.2)
        return [msg for msg in self.order_messages if msg['orderId'] == order_id]

    def disconnect(self):
        self.connection.eDisconnect()



