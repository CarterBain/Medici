__author__ = 'oglebrandon'
from ib.ext.EWrapper import EWrapper
from ib.client.Portfolio import Account, AccountMessage
import logging as logger
import sys
import types


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


class SyncWrapper(EWrapper, Observable):
    suppress = False
    emitter = []
    account = Account()
    ref_id = None

    def __init__ (self,subs={}):
        super(SyncWrapper, self).__init__()
        self.subscriptions = subs


    # def setSubscriptions (self,subs):
    #     self.subscriptions = subs

    def accountDownloadEnd(self, accountName):
        if 'accountDownloadEnd' in self.emitter:
            msg = {'accountName' : accountName}
            
        
        if self.suppress is False:
            showmessage('accountDownloadEnd', vars())

    def bondContractDetails(self, reqId, contractDetails):
        if 'bondContractDetails' in self.emitter:
            msg = {'reqId' : reqId,
                    'contractDetails' : contractDetails}
            
        
        if self.suppress is False:
            showmessage('bondContractDetails', vars())

    def commissionReport(self, commissionReport):
        if 'commissionReport' in self.emitter:
            msg = {'commissionReport' : commissionReport}
            
        
        if self.suppress is False:
            showmessage('commissionReport', vars())

    def connectionClosed(self):
        if 'connectionClosed' in self.emitter:
            msg = {}
            
        
        if self.suppress is False:
            showmessage('connectionClosed', vars())

    def contractDetails(self, reqId, contractDetails):
        if 'contractDetails' in self.emitter:
            msg = {'reqId' : reqId,
                    'contractDetails' : contractDetails}
            
        
        if self.suppress is False:
            showmessage('contractDetails', vars())

    def contractDetailsEnd(self, reqId):
        if 'contractDetailsEnd' in self.emitter:
            msg = {'reqId' : reqId}
            
        
        if self.suppress is False:
            showmessage('contractDetailsEnd', vars())

    def currentTime(self, time):
        if 'currentTime' in self.emitter:
            msg = {'time' : time}
            
        
        if self.suppress is False:
            showmessage('currentTime', vars())

    def deltaNeutralValidation(self, reqId, underComp):
        if 'deltaNeutralValidation' in self.emitter:
            msg = {'reqId' : reqId,
                    'underComp' : underComp}
            
        
        if self.suppress is False:
            showmessage('deltaNeutralValidation', vars())

    def error_0(self, strval):
        if 'error_0' in self.emitter:
            msg = {'strval' : strval}
            
        
        if self.suppress is False:
            showmessage('error_0', vars())

    def error_1(self, id, errorCode, errorMsg):
        if 'error_1' in self.emitter:
            msg = {'id' : id,
                    'errorCode' : errorCode,
                    'errorMsg' : errorMsg}
            
        
        if self.suppress is False:
            showmessage('error_1', vars())

    def execDetails(self, reqId, contract, execution):
        if 'execDetails' in self.emitter:
            msg = {'reqId' : reqId,
                    'contract' : contract,
                    'execution' : execution}
            
        
        if self.suppress is False:
            showmessage('execDetails', vars())

    def execDetailsEnd(self, reqId):
        if 'execDetailsEnd' in self.emitter:
            msg = {'reqId' : reqId}
            
        
        if self.suppress is False:
            showmessage('execDetailsEnd', vars())

    def fundamentalData(self, reqId, data):
        if 'fundamentalData' in self.emitter:
            msg = {'reqId' : reqId,
                    'data' : data}
            
        
        if self.suppress is False:
            showmessage('fundamentalData', vars())

    def historicalData(self, reqId, date, open, high, low, close, volume, count, WAP, hasGaps):
        if 'historicalData' in self.emitter:
            msg = {'reqId'   : reqId,
                    'date'   : date,
                    'open'   : open,
                    'high'   : high,
                    'low'    : low,
                    'close'  : close,
                    'volume' : volume,
                    'count'  : count,
                    'WAP'    : WAP,
                    'hasGaps': hasGaps}
            
        
        if self.suppress is False:
            showmessage('historicalData', vars())

    def managedAccounts(self, accountsList):
        if 'managedAccounts' in self.emitter:
            msg = {'accountsList' : filter(None, accountsList.split(','))}
            
        
        if self.suppress is False:
            showmessage('managedAccounts', vars())

    def marketDataType(self, reqId, marketDataType):
        if 'marketDataType' in self.emitter:
            msg = {'reqId' : reqId,
                    'marketDataType' : marketDataType}
            
        
        if self.suppress is False:
            showmessage('marketDataType', vars())

    def nextValidId(self, orderId):
        if 'nextValidId' in self.emitter:
            msg = {'orderId' : orderId}
            
        
        if self.suppress is False:
            showmessage('nextValidId', vars())

    def openOrder(self, orderId, contract, order, orderState):
        if 'openOrder' in self.emitter:
            msg = {'orderId' : orderId,
                    'contract' : contract,
                    'order' : order,
                    'orderState' : orderState}
            
        
        if self.suppress is False:
            showmessage('openOrder', vars())

    def openOrderEnd(self):
        if 'openOrderEnd' in self.emitter:
            msg = {}
            
        
        if self.suppress is False:
            showmessage('openOrderEnd', vars())

    def orderStatus(self, orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld):
        if 'orderStatus' in self.emitter:
            msg = {'orderId' : orderId,
                    'status' : status,
                    'filled' : filled,
                    'remaining' : remaining,
                    'avgFillPrice' : avgFillPrice,
                    'permId' : permId,
                    'parentId' : parentId,
                    'lastFillPrice' : lastFillPrice,
                    'clientId' : clientId,
                    'whyHeld' : whyHeld}
            
        
        if self.suppress is False:
            showmessage('orderStatus', vars())

    def realtimeBar(self, reqId, time, open, high, low, close, volume, wap, count):
        if 'realtimeBar' in self.emitter:
            msg = {'reqId' : reqId,
                    'time' : time,
                    'open' : open,
                    'high' : high,
                    'low' : low,
                    'close' : close,
                    'volume' : volume,
                    'wap' : wap,
                    'count' : count}
            
        
        if self.suppress is False:
            showmessage('realtimeBar', vars())

    def receiveFA(self, faDataType, xml):
        if 'receiveFA' in self.emitter:
            msg = {'faDataType' : faDataType,
                    'xml' : xml}
            
        
        if self.suppress is False:
            showmessage('receiveFA', vars())

    def scannerData(self, reqId, rank, contractDetails, distance, benchmark, projection, legsStr):
        if 'scannerData' in self.emitter:
            msg = {'reqId' : reqId,
                    'rank' : rank,
                    'contractDetails' : contractDetails,
                    'distance' : distance,
                    'benchmark' : benchmark,
                    'projection' : projection,
                    'legsStr' : legsStr}
            
        
        if self.suppress is False:
            showmessage('scannerData', vars())

    def scannerDataEnd(self, reqId):
        if 'scannerDataEnd' in self.emitter:
            msg = {'reqId' : reqId}
            
        
        if self.suppress is False:
            showmessage('scannerDataEnd', vars())

    def scannerParameters(self, xml):
        if 'scannerParameters' in self.emitter:
            msg = {'xml' : xml}
            
        
        if self.suppress is False:
            showmessage('scannerParameters', vars())

    def tickEFP(self, tickerId, tickType, basisPoints, formattedBasisPoints, impliedFuture, holdDays, futureExpiry, dividendImpact, dividendsToExpiry):
        if 'tickEFP' in self.emitter:
            msg = {'tickerId' : tickerId,
                    'tickType' : tickType,
                    'basisPoints' : basisPoints,
                    'formattedBasisPoints' : formattedBasisPoints,
                    'impliedFuture' : impliedFuture,
                    'holdDays' : holdDays,
                    'futureExpiry' : futureExpiry,
                    'dividendImpact' : dividendImpact,
                    'dividendsToExpiry' : dividendsToExpiry}
            
        
        if self.suppress is False:
            showmessage('tickEFP', vars())

    def tickGeneric(self, tickerId, tickType, value):
        if 'tickGeneric' in self.emitter:
            msg = {'tickerId' : tickerId,
                    'tickType' : tickType,
                    'value' : value}
            
        
        if self.suppress is False:
            showmessage('tickGeneric', vars())

    def tickOptionComputation(self, tickerId, field, impliedVol, delta, optPrice, pvDividend, gamma, vega, theta, undPrice):
        if 'tickOptionComputation' in self.emitter:
            msg = {'tickerId' : tickerId,
                    'field' : field,
                    'impliedVol' : impliedVol,
                    'delta' : delta,
                    'optPrice' : optPrice,
                    'pvDividend' : pvDividend,
                    'gamma' : gamma,
                    'vega' : vega,
                    'theta' : theta,
                    'undPrice' : undPrice}
            
        
        if self.suppress is False:
            showmessage('tickOptionComputation', vars())

    def tickPrice(self, tickerId, field, price, canAutoExecute):
        if 'tickPrice' in self.emitter:
            msg = {'tickerId' : tickerId,
                    'field' : field,
                    'price' : price,
                    'canAutoExecute' : canAutoExecute}
            
        
        if self.suppress is False:
            showmessage('tickPrice', vars())

    def tickSize(self, tickerId, field, size):
        if 'tickSize' in self.emitter:
            msg = {'tickerId' : tickerId,
                    'field' : field,
                    'size' : size}
            
        
        if self.suppress is False:
            showmessage('tickSize', vars())

    def tickSnapshotEnd(self, reqId):
        if 'tickSnapshotEnd' in self.emitter:
            msg = {'reqId' : reqId}
            
        
        if self.suppress is False:
            showmessage('tickSnapshotEnd', vars())

    def tickString(self, tickerId, tickType, value):
        if 'tickString' in self.emitter:
            msg = {'tickerId' : tickerId,
                    'tickType' : tickType,
                    'value' : value}
            
        
        if self.suppress is False:
            showmessage('tickString', vars())

    def updateAccountTime(self, timeStamp):
        if 'updateAccountTime' in self.emitter:
            msg = {'timeStamp' : timeStamp}
            
        
        if self.suppress is False:
            showmessage('updateAccountTime', vars())

    def updateAccountValue(self, key, value, currency, accountName):

        msg = AccountMessage(key, value, currency)

        if 'REQUEST FAILED' in self.account[self.ref_id].messages:
            self.account[self.ref_id].messages[0] = msg
        else:
            self.account[self.ref_id].add_message(msg)
        if self.suppress is False:
            showmessage('updateAccountValue', vars())

    def updateMktDepth(self, tickerId, position, operation, side, price, size):
        if 'updateMktDepth' in self.emitter:
            msg = {'tickerId' : tickerId,
                    'position' : position,
                    'operation' : operation,
                    'side' : side,
                    'price' : price,
                    'size' : size}
            
        
        if self.suppress is False:
            showmessage('updateMktDepth', vars())

    def updateMktDepthL2(self, tickerId, position, marketMaker, operation, side, price, size):
        if 'updateMktDepthL2' in self.emitter:
            msg = {'tickerId' : tickerId,
                    'position' : position,
                    'marketMaker' : marketMaker,
                    'operation' : operation,
                    'side' : side,
                    'price' : price,
                    'size' : size}
            
        
        if self.suppress is False:
            showmessage('updateMktDepthL2', vars())

    def updateNewsBulletin(self, msgId, msgType, message, origExchange):
        if 'updateNewsBulletin' in self.emitter:
            msg = {'msgId' : msgId,
                    'msgType' : msgType,
                    'message' : message,
                    'origExchange' : origExchange}
            
        
        if self.suppress is False:
            showmessage('updateNewsBulletin', vars())

    def updatePortfolio(self, contract, position, marketPrice, marketValue, averageCost, unrealizedPNL, realizedPNL, accountName):
        if 'updatePortfolio' in self.emitter:
            msg = {'contract' : contract,
                    'position' : position,
                    'marketPrice' : marketPrice,
                    'marketValue' : marketValue,
                    'averageCost' : averageCost,
                    'unrealizedPNL' : unrealizedPNL,
                    'realizedPNL' : realizedPNL,
                    'accountName' : accountName}
            
        
        if self.suppress is False:
            showmessage('updatePortfolio', vars())

    def error(self, id=None, errorCode=None, errorMsg=None):
        if 'error' in self.emitter:
            msg = {'id' : id,
                   'errorCode' : errorCode,
                   'errorMsg' : errorMsg}
            
        
        if self.suppress is False:
            showmessage('error', vars())


