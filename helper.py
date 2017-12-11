import time

def bbDateTounixDate( date):
    return time.mktime( time.strptime(date, "%m/%d/%Y"))

#
def myDateTounixDate( date):
    return time.mktime( time.strptime(date, "%Y%m%d"))

#
def unixDateTomyDate( unixdate):
    return time.strftime( "%Y%m%d", time.localtime( unixdate))
#

def unixDateTobbDate( unixdate):
    return time.strftime( "%m/%d/%Y", time.localtime( unixdate))
#
def unixDateTomySqlDate( unixdate):
    return time.strftime( "%Y/%m/%d", time.localtime( unixdate))
#
def incrementDate( date, days):
    if "/" in date:
        unix_date = bbDateTounixDate( date)
    else:
        unix_date = myDateTounixDate( date)
    #    
    unix_date += days * 24 * 60 * 60
    return unixDateTomyDate( unix_date)
#
def list2Dict( lis,lisOflis=None):
    d = {}
    for tok in lis:
        if not lisOflis:
            d[tok[0]] = tok[1]
        else:
            d[tok[0]] = tok[1:]
    #
    return d
