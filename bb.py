#############################################
######### INTERFACE TO OLDER bb.py ##########
#############################################
#
# BBDataRequest.py is the latest python API
# to connect to bloomberg. The output from
# this module is more useful (with correct
# types etc) than that of bb.py. But our older
# code use bb.py(old) and we don't want to
# break anything by switching to the new API.
# So this module is to act as an interface (Facade)
# to the new BBDataRequest.py. This will return
# the data in the same format as the bb.py(old)
#
#################################################


NEW_API = True

if NEW_API:
    print "\n*** Using latest version of Bloomberg Python API ***\n"
    import datetime, imp
    bbdr = imp.load_source("bbdr", "G:\\BBPython\\BBDataRequest.py")

    # Historical Arguments - Relevant

    # startDate                   string  ST
    #
    # endDate                     string  END
    #
    # periodicityAdjustment       string  NR
    #     ACTUAL
    #     CALENDAR
    #     FISCAL
    #
    # periodicitySelection        string  PD
    #      DAILY
    #      WEEKLY
    #      MONTHLY
    #      QUARTERLY
    #      SEMI_ANNUALLY
    #      YEARLY
    #
    # currency                    string  CCY
    #
    # nonTradingDayFillOption     string  ?
    #      NON_TRADING_WEEKDAYS
    #      ALL_CALENDAR_DAYS
    #      ACTIVE_DAYS_ONLY
    #
    # nonTradingDayFillMethod     string  ?
    #      PREVIOUS_VALUE
    #      NIL_VALUE


    class BBConnection:
        def __init__(self, connection_type="S", timeout_wait=30):
            pass
        
        def request( self, bbstr):
            ticker, rstr = bbstr.strip().split(",[")
            if rstr[-1] == ']':         #static request
                fields = rstr[:-1].split(",")
                bbout = bbdr.bbRequest(ticker, fields)
                bblis = bbout[ticker]
                modlis = []
                #print "***",bblis
                for j in bblis:
                    if isinstance(j, datetime.date):
                        modlis.append(j.strftime("%m/%d/%Y"))
                    elif isinstance(j, datetime.time):
                        modlis.append(j.strftime("%H:%M"))
                    elif isinstance(j, str):
                        modlis.append(j)
                    elif isinstance(j, (float, int, long)):
                        modlis.append(str(j))
                    else:
                        modlis.append(j)
                    #
                #
                return [modlis]
                #return [map(str, bbout[ticker])]
            else: # Historic request
                fields = rstr.split("],")[0].split(",")
                hargstr = rstr.split("],")[1]
                hargDict = {}
                for harg in hargstr.split():
                    ky,val = harg.split("=")
                    if ky == 'ST' :hargDict["startDate"] = val
                    if ky == 'END':hargDict["endDate"] = val
                    if ky == 'NR' :
                        if val in ('C'):
                            hargDict["periodicityAdjustment"] = 'CALENDAR'
                        elif val in ('T','A'):
                            hargDict["periodicityAdjustment"] = 'ACTUAL'
                        #
                    #
                    if ky == 'PD' :
                        if val == 'D':
                            hargDict["periodicitySelection"] = 'DAILY'
                        else:
                            hargDict["periodicitySelection"] = val
                        #
                    if ky == 'CCY':hargDict["currency"] = val
                #
                bbout = bbdr.bbHistRequest(ticker, fields, **hargDict)
                bblis = bbout[ticker]
                if not bblis:return [[datetime.date.today().strftime("%m/%d/%Y"), '#N/A History']]
                modlis = []
                for i in bblis:
                    tlis = []
                    for j in i:
                        if isinstance(j, datetime.date):
                            tlis.append(j.strftime("%m/%d/%Y"))
                        elif isinstance(j, str):
                            tlis.append(j)
                        elif isinstance(j, (float, int)):
                            tlis.append(str(j))
                        else:
                            tlis.append(j)
                        #
                    #
                    modlis.append( tlis)
                #
                return modlis
            #
        #
    
else:
    print "\n*** Using older version of Bloomberg Python API bb.py(old/dde) ***\n"
    import imp
    bb = imp.load_source("bb", "bb.py")
    from bb import BBConnection
    
