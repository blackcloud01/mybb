import imp
bb = imp.load_source("bb", "G:\\BBPython\\bb.py")
#import bb

# Global Bloomberg Historical Query Connection
bbc = bb.BBConnection("H")
import time
def getHistoricalData( symbol, bbfield, startDate, endDate, currency=None, periodicity="D", norm="A",filler=None):
    bbstring = symbol + ",[" + bbfield + "]," + "ST=%s END=%s PD=%s NR=%s "%( startDate, endDate, periodicity, norm)
    if currency:
        bbstring += "CCY="+currency
    #
    if filler:
        bbstring += " FL="+filler
    #
    #print bbstring
    res = bbc.request( bbstring)
    #print res
    return res
#
def getHistoricalData_new( symbol, bbfield, startDate, endDate, currency=None, periodicity="D", norm="A"):
    bbstring = symbol + ",[" + bbfield + "]," + "ST=%s END=%s PD=%s NR=%s "%( startDate, endDate, periodicity, norm)
    if currency:
        bbstring += "CCY="+currency
    #
    res = None
    c = 0
    while not res:
        c += 1
        try:
            res = bbc.request( bbstring)
        except:
            pass
        #
        if not res:
            print bbc
            del bbc
            bbc = bb.BBConnection("H")
        #
        if c == 10:
            sys.stderr.writelines("BB request fail even after many attempts!\n")
            break
    #
    return res

#
def bbDateTounixDate( date):
    return time.mktime( time.strptime(date, "%m/%d/%Y"))

#
def myDateTounixDate( date):
    return time.mktime( time.strptime(date, "%Y%m%d"))

#
def unixDateTomyDate( unixdate):
    return time.strftime( "%Y%m%d", time.localtime( unixdate))
#

def incrementDate( date, days):
    if "/" in date:
        unix_date = bbDateTounixDate( date)
    else:
        unix_date = myDateTounixDate( date)
    #    
    unix_date += days * 24 * 60 * 60
    return unixDateTomyDate( unix_date)
