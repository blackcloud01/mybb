#####################################
# CONNECTION TO BLOOMBERG API       #
#####################################


import blpapi
from optparse import OptionParser


def parseCmdLine():
    parser = OptionParser(description="Retrieve reference data.")
    parser.add_option("-a",
                      "--ip",
                      dest="host",
                      help="server name or IP (default: %default)",
                      metavar="ipAddress",
                      default="localhost")
    parser.add_option("-p",
                      dest="port",
                      type="int",
                      help="server port (default: %default)",
                      metavar="tcpPort",
                      default=8194)

    (options, args) = parser.parse_args()

    return options


# Set up connection
global options
options = parseCmdLine()

# Fill SessionOptions
sessionOptions = blpapi.SessionOptions()
sessionOptions.setServerHost(options.host)
sessionOptions.setServerPort(options.port)

print "Connecting to %s:%d" % (options.host, options.port)

# Create a Session
session = blpapi.Session(sessionOptions)

# Start a Session
if not session.start():
    print "Failed to start session."
    raise

if not session.openService("//blp/refdata"):
    print "Failed to open //blp/refdata"
    raise

refDataService = session.getService("//blp/refdata")




def processMessage( ReferenceDataResponse, fields):
    if ReferenceDataResponse.hasElement("responseError"):
        print "Response Error:", ReferenceDataResponse
        return
    securityDataArray = ReferenceDataResponse.getElement("securityData")
    numItems = securityDataArray.numValues()
    secFldDict = {}
    for i in range(numItems):
        securityData = securityDataArray.getValueAsElement(i)
        if securityData.hasElement("securityError"):
            print "Security Error:", securityData
            continue
        #
        security = securityData.getElementAsString("security")
        fieldData = securityData.getElement("fieldData")
        secFldData = []
        if type(fields) == type([]):
            for fld in fields:
                if fieldData.hasElement(fld):
                    fdata = fieldData.getElementValue( fld)
                else:
                    fdata = "#N/A N.A."
                #
                secFldData.append( fdata)
        else:
            if fieldData.hasElement(fields):
                fdata = fieldData.getElementValue( fields)
            else:
                fdata = "#N/A N.A."
            #
            secFldData.append( fdata)
        #
        secFldDict[security] = secFldData
    #
    return secFldDict
#

def bbRequest( ticker, field):
    request = refDataService.createRequest("ReferenceDataRequest")
    # if the ticker is a list of tickers add request to each
    if type(ticker) == type([]):
        for symbol in ticker:
            request.append("securities", symbol)
    else:
        request.append("securities", ticker)
    #
    # if field is a list of fields add request to each
    if type(field) == type([]):
        for fld in field:
            request.append("fields", fld)
    else:
        request.append("fields", field)
    #
    # Send the request
    session.sendRequest(request)

    outDict = {}
    try:
        # Process received events
        while(True):
            # We provide timeout to give the chance to Ctrl+C handling:
            event = session.nextEvent(500)
            for ReferenceDataResponse in event:
                #print ReferenceDataResponse
                if ReferenceDataResponse.hasElement("securityData"):
                    outDict.update(processMessage( ReferenceDataResponse, field))
            # Response completly received, so we could exit
            if event.eventType() == blpapi.Event.RESPONSE:
                break
            
    finally:
        pass
    #
    return outDict
#
def processBulkMessage( ReferenceDataResponse, fields):
    if ReferenceDataResponse.hasElement("responseError"):
        print "Response Error:", ReferenceDataResponse
        return
    securityDataArray = ReferenceDataResponse.getElement("securityData")
    numItems = securityDataArray.numValues()
    secFldDict = {}
    for i in range(numItems):
        securityData = securityDataArray.getValueAsElement(i)
        if securityData.hasElement("securityError"):
            print "Security Error:", securityData
            continue
        #
        security = securityData.getElementAsString("security")
        fieldData = securityData.getElement("fieldData")
        outData = []
        try:
            bulkData = fieldData.getElement( 0)
        except:
            print "No Bulkdata"
            continue
        #
        numRows = bulkData.numValues()
        for i in range(numRows):
            bdata = bulkData.getValue(i)
            numBItems = bdata.numElements()
            biter = bdata.elements()
            brow = []
            for bctr in range( numBItems):
                bitem = biter.next()
                if bitem.isNull():
                    brow.append(None)
                else:
                    brow.append(bitem.getValue(0))
            #
            outData.append( brow)
        #
        secFldDict[security] = outData
    #
    return secFldDict
#

def bbBulkRequest( ticker, field):
    request = refDataService.createRequest("ReferenceDataRequest")
    # if the ticker is a list of tickers add request to each
    if type(ticker) == type([]):
        for symbol in ticker:
            request.append("securities", symbol)
    else:
        request.append("securities", ticker)
    #
    # if field is a list of fields add request to each
    if type(field) == type([]):
        for fld in field:
            request.append("fields", fld)
    else:
        request.append("fields", field)
    #
    # Send the request
    session.sendRequest(request)

    outDict = {}
    try:
        # Process received events
        while(True):
            # We provide timeout to give the chance to Ctrl+C handling:
            event = session.nextEvent(500)
            for ReferenceDataResponse in event:
                #print ReferenceDataResponse
                if ReferenceDataResponse.hasElement("securityData"):
                    outDict.update(processBulkMessage( ReferenceDataResponse, field))
            # Response completly received, so we could exit
            if event.eventType() == blpapi.Event.RESPONSE:
                break
            
    finally:
        pass
    #
    return outDict

#
def processHistMessage( HistoricalDataResponse, fields):
    if HistoricalDataResponse.hasElement("responseError"):
        print "Response Error:", HistoricalDataResponse
        return
    secFldDict = {}
    securityData = HistoricalDataResponse.getElement("securityData")
    security = securityData.getElementAsString("security")
    histDataArray = securityData.getElement("fieldData")
    numFields = histDataArray.numValues()
    secFldData = []
    for j in range( numFields):
        histDataRow = histDataArray.getValueAsElement(j)
        numData = histDataRow.numElements()
        date = histDataRow.getElementAsDatetime("date")
        dateData=[date]
        if type(fields) == list:
            for fld in fields:
                if histDataRow.hasElement(fld):
                    fdata = histDataRow.getElementValue(fld)
                else:
                    fdata = "#N/A N.A."
                #
                dateData.append( fdata)
            #
        else:
            if histDataRow.hasElement(fields):
                fdata = histDataRow.getElementValue(fields)
            else:
                fdata = "#N/A N.A."
            #
            dateData.append( fdata)
        
        #
        secFldData.append(dateData)
    #
    secFldDict[security] = secFldData
    #
    return secFldDict
#

def bbHistRequest( ticker, field, **hargs):
    request = refDataService.createRequest("HistoricalDataRequest")
    # if the ticker is a list of tickers add request to each
    if type(ticker) == type([]):
        for symbol in ticker:
            request.append("securities", symbol)
    else:
        request.append("securities", ticker)
    #
    # if field is a list of fields add request to each
    if type(field) == type([]):
        for fld in field:
            request.append("fields", fld)
    else:
        request.append("fields", field)
    #
    for ky,val in hargs.items():request.set( ky, val)
    # Send the request
    session.sendRequest(request)

    outDict = {}
    try:
        # Process received events
        while(True):
            # We provide timeout to give the chance to Ctrl+C handling:
            event = session.nextEvent(500)
            for HistoricalDataResponse in event:
                if HistoricalDataResponse.hasElement("securityData"):
                    outDict.update(processHistMessage( HistoricalDataResponse, field))
                #
            #
            # Response completly received, so we could exit
            if event.eventType() == blpapi.Event.RESPONSE:
                break
            
    finally:
        pass
    #
    return outDict


if __name__ == '__main__':

    # Sample Test Cases
    
    d = bbRequest(["IBM Equity", "VOD LN Equity"], ["PX_LAST","NEWS_HEAT_STORY_FLOW_RT"])
    print d

    d = bbRequest("ACA FP Equity", ["MOST_RECENT_PERIOD_END_DT","NEWS_HEAT_STORY_FLOW_RT"])
    print d

    d = bbBulkRequest("TEF SQ Equity", "BDVD_ALL_PROJECTIONS")
    print d

    d = bbBulkRequest("TEF SQ Equity", "EQY_DVD_HIST_GROSS")
    print d

    dh = bbHistRequest(["IBM Equity", "MKC Equity"], ["PX_LAST","NEWS_HEAT_PUB_DNUMSTORIES","NEWS_HEAT_PUB_DAVG"], startDate="20140505", endDate="20140625", currency="USD")
    print dh

    dh = bbHistRequest("GBP Curncy", ["PX_LAST"], startDate="20140605", endDate="20140611")
    print dh

    dh = bbHistRequest("ACA FP Equity", ["CF_CASH_FROM_OPER"], startDate="20080101", periodicitySelection="MONTHLY")
    print dh
    

