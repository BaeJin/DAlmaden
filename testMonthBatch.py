import datetime
from dateutil.relativedelta import relativedelta

fromdate = '2010-03-14'
todate = '2014-05-07'

fromdate = datetime.datetime.strptime(fromdate,'%Y-%m-%d')
todate = datetime.datetime.strptime(todate,'%Y-%m-%d')
yearDifference = todate.year*12 - fromdate.year*12
monthDifference = todate.month - fromdate.month
periodDfference = yearDifference + monthDifference
#
monthBatch_list = []
for monthdelta in range(0,periodDfference+1):

    ##1달을 지정한다
    one_month = relativedelta(months=monthdelta)
    monthBatch = fromdate + one_month
    monthBatch = monthBatch.strftime('%Y-%m')
    monthBatch_list.append(monthBatch)

print(monthBatch_list)