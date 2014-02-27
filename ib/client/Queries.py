__author__ = 'oglebrandon'


class Contracts(object):
    store = {}

    def append(self, ref, contract):
        if ref in self.store:
            self.store[ref].append(contract)
        else:
            self.store[ref] = [contract]

    def __getitem__(self, ref):
        return self.store[ref]
