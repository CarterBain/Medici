__author__ = 'oglebrandon'


class Contracts(object):
    store = {}

    def append(self, ref, contract):
        self.store[ref] = contract

    def __getitem__(self, ref):
        return self.store[ref]
