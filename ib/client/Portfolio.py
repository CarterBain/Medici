__author__ = 'oglebrandon'

class Account(object):
    def __init__(self):
        self._packets = {}
    def __getitem__(self, ref):
        return self._packets[ref]

    def append_request(self, ref, request):
        self._packets[ref] = request

class AccountPacket(object):
    def __init__(self, acct_num, requested=None):
        self.acct_num = acct_num
        self.requested = requested
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