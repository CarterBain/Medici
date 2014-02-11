__author__ = 'oglebrandon'

import logging as logger
import types
from ib.ext.EWrapper import EWrapper

def showmessage(message, mapping):
    try:
        del(mapping['self'])
    except (KeyError, ):
        pass
    items = mapping.items()
    items.sort()
    print '### %s' % (message, )
    for k, v in items:
        print '    %s:%s' % (k, v)


class Observable(object):
    """
    Sender -> dispatches messages to interested callables
    """
    def __init__(self):
        self.listeners = {}
        self.logger = logger.getLogger()


    def register(self,listener,events=None):
        """
        register a listener function

        Parameters
        -----------
        listener : external listener function
        events  : tuple or list of relevant events (default=None)
        """
        if events is not None and type(events) not in \
                (types.TupleType,types.ListType):
            events = (events,)

        self.listeners[listener] = events

    def dispatch(self,event=None, msg=None):
        """notify listeners """
        for listener,events in self.listeners.items():
            if events is None or event is None or event in events:
                try:
                    listener(self,event,msg)
                except (Exception,):
                    self.unregister(listener)
                    errmsg = "Exception in message dispatch: Handler '{0}' " \
                             "unregistered for event " \
                             "'{1}'  ".format(listener.func_name,event)
                    self.logger.exception(errmsg)

    def unregister(self,listener):
        """ unregister listener function """
        del self.listeners[listener]

class ReferenceWrapper(EWrapper,Observable):

    # contract = None
    # tickerId
    # field
    # price


    def __init__ (self,subs={}):
        super(ReferenceWrapper, self).__init__()
        self.orderID = None
        self.subscriptions = subs

    def setSubscriptions (self,subs):
        self.subscriptions = subs

    def tickGeneric(self, tickerId, field, price):
        pass

    def tickPrice(self, tickerId, field, price, canAutoExecute):
        showmessage('tickPrice', vars())

    def tickSize(self, tickerId, field, size):
        showmessage('tickSize', vars())


    def tickString(self, tickerId, tickType, value):
        #showmessage('tickString', vars())
        pass

    def tickOptionComputation(self, tickerId, field,
                              impliedVolatility, delta,
                              x, c, q, w, e, r):
        #showmessage('tickOptionComputation', vars())
        pass

    def openOrderEnd(self):
        pass

    def orderStatus(self, orderId, status, filled, remaining,
                    avgFillPrice, permId, parentId, lastFillPrice,
                    clientId, whyHeId):

        if filled:
            self.dispatch(event='execution',msg=[1,2,3])
        showmessage('orderStatus', vars())

    def openOrder(self, orderId, contract, order, state):
        showmessage('openOrder', vars())

    def connectionClosed(self):
        showmessage('connectionClosed', {})

    def updateAccountValue(self, key, value, currency, accountName):
        showmessage('updateAccountValue', vars())

    def updatePortfolio(self, contract, position, marketPrice,
                        marketValue, averageCost, unrealizedPNL,
                        realizedPNL, accountName):
        showmessage('updatePortfolio', vars())

    def updateAccountTime(self, timeStamp):
        showmessage('updateAccountTime', vars())

    def nextValidId(self, orderId):
        self.orderID = orderId
        showmessage('nextValidId', vars())

    def contractDetails(self, reqId, contractDetails):
        showmessage('contractDetails', vars())
        print contractDetails.__dict__

    def bondContractDetails(self, reqId, contractDetails):
        showmessage('bondContractDetails', vars())

    def execDetails(self, orderId, contract, execution):
        showmessage('execDetails', vars())

    def error(self, id=None, errorCode=None, errorMsg=None):
        showmessage('error', vars())

    def updateMktDepth(self, tickerId, position, operation, side, price, size):
        showmessage('updateMktDepth', vars())

    def updateMktDepthL2(self, tickerId, position,
                         marketMaker, operation,
                         side, price, size):
        showmessage('updateMktDepthL2', vars())

    def updateNewsBulletin(self, msgId, msgType, message, origExchange):
        showmessage('updateNewsBulletin', vars())

    def managedAccounts(self, accountsList):
        showmessage('managedAccounts', vars())

    def receiveFA(self, faDataType, xml):
        showmessage('receiveFA', vars())

    def historicalData(self, reqId, date,
                       open, high, low, close,
                       volume, count, WAP, hasGaps):
        showmessage('historicalData', vars())

    def scannerParameters(self, xml):
        showmessage('scannerParameters', vars())

    def scannerData(self, reqId, rank, contractDetails,
                    distance, benchmark, projection, legsStr):
        showmessage('scannerData', vars())

    def accountDownloadEnd(self, accountName):
        showmessage('accountDownloadEnd', vars())

    def contractDetailsEnd(self, reqId):
        showmessage('contractDetailsEnd', vars())

    def currentTime(self):
        showmessage('currentTime', vars())

    def deltaNeutralValidation(self):
        showmessage('deltaNeutralValidation', vars())

    def error_0(self):
        showmessage('error_0', vars())

    def error_1(self):
        showmessage('error_1', vars())

    def execDetailsEnd(self):
        showmessage('execDetailsEnd', vars())

    def fundamentalData(self):
        showmessage('fundamentalData', vars())

    def realtimeBar(self):
        showmessage('realtimeBar', vars())

    def scannerDataEnd(self):
        showmessage('scannerDataEnd', vars())

    def tickEFP(self):
        showmessage('tickEFP', vars())

    def tickSnapshotEnd(self):
        showmessage('tickSnapshotEnd', vars())

    def marketDataType(self):
        showmessage('marketDataType', vars())

    def commissionReport(self, commissionReport):
        showmessage('commissionReport', vars())