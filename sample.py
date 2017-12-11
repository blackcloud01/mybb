import imp

bbdr = imp.load_source("bbdr", "L:\BBPython\BBDataRequest.py")


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



