__author__ = 'oglebrandon'

class Contracts(object):
    store = {}

    def append(self, ref, contract):
        self.store[ref] = contract
