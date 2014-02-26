# from dateutil import parser


# from pandas.lib import Timestamp

from time import sleep
import uuid

import numpy as np

from ib.client.Portfolio import AccountPacket, PortfolioPacket
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
        sleep(.2)

    def request_reference_id(self, integer=False):
        """
        Provides a unique reference id.

        Returns a unique classifier ID, used to reference a
        return message.

        Parameters
        ----------
        integer : bool, optional
            if True, the resulting reference ID is a unique
            random integer (0,999999999), otherwise a unique
            UUID is used (default)

        Returns
        -------
        return_value : str or int
            Unique reference ID

        Notes
        -----
        This function generates a random ID and checks against
        self.ref_nums to ensure it is unique, else the function
        calls itself until a unique identifier is found


        Examples
        --------
        >>> IBClient.request_reference_id(integer=True)
        101010101 # random
        """

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

    def method(self, sender, event, msg=None):
        print "[{0}] got event {1} with message {2}".format(self.name, event, msg)

    # def __flatten__(self, container):
    #     """
    #     Flattens an arbitrarily nested object
    #     """
    #     for i in container:
    #         if isinstance(i, list) or isinstance(i, tuple):
    #             for j in self.__flatten__(i):
    #                 yield j
    #         else:
    #             yield i

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

    # def orders(self):


    def disconnect(self):
        self.connection.eDisconnect()


client = IBClient(call_msg=False)
sleep(2)
client.disconnect()

