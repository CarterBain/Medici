__author__ = 'oglebrandon'

class Account(object):
    def __init__(self):
        self._packets = {}
    def __getitem__(self, ref):
        return self._packets[ref]

    def append_request(self, ref, acct_packet, port_packet):
        self._packets[ref] = {'account': acct_packet, 'portfolio': port_packet}

class AccountPacket(object):
    def __init__(self, acct_num, requested=None):
        self.acct_num = acct_num
        #self.requested = requested
        self.messages = []
        self.add_message('REQUEST FAILED')

    def add_message(self, msg):
        self.messages.append(msg)

class AccountMessage(object):
    def __init__(self, key, value, currency):
        self.key = key
        self.value = value
        self.currency = currency

    def __repr__(self):
        self.msg = (self.key, self.value, self.currency)
        return str(self.msg)
        #self.datetime = dt.datetime.utcnow()

class PortfolioPacket(object):
    def __init__(self, acct_num, requested=None):
        self.acct_num = acct_num
        #self.requested = requested
        self.messages = []
        self.add_message('REQUEST FAILED')

    def add_message(self, msg):
        self.messages.append(msg)

class PortfolioMessage(object):
    def __init__(self, contract, position, marketPrice, marketValue, averageCost, unrealizedPNL, realizedPNL, accountName):
       self.contract = contract
       self.position = position
       self.market_price = marketPrice
       self.market_value = marketValue
       self.avg_cost = averageCost
       self.unrealized_pnl = unrealizedPNL
       self.realized_pnl = realizedPNL
       self.account_name = accountName

    def __repr__(self):
        self.msg =  {'contract': self.contract,
                     'position_size' : self.position,
                     'market_price' : self.market_price,
                     'market_value' : self.market_value,
                     'average_cost' : self.avg_cost,
                     'unrealized pnl':self.unrealized_pnl,
                     'realized pnl' : self.realized_pnl,
                     'account' : self.account_name}
        return str(self.msg)
        #self.datetime = dt.datetime.utcnow()