from datetime import datetime
from dateutil.relativedelta import relativedelta


class DateCalculator:
    def calcDatetime(self,dtNow, dtDiff):
        if 'years ago' in dtDiff:
            d = int(dtDiff.split(' ')[0])
            dtPub = dtNow - relativedelta(years=d)
        elif 'months ago' in dtDiff:
            d = int(dtDiff.split(' ')[0])
            dtPub = dtNow - relativedelta(months=d)
        elif 'weeks ago' in dtDiff:
            d = int(dtDiff.split(' ')[0])
            dtPub = dtNow - relativedelta(weeks=d)
        elif 'days ago' in dtDiff:
            d = int(dtDiff.split(' ')[0])
            dtPub = dtNow - relativedelta(days=d)
        elif 'hours ago' in dtDiff:
            d = int(dtDiff.split(' ')[0])
            dtPub = dtNow - relativedelta(hours=d)
        elif 'minutes ago' in dtDiff:
            d = int(dtDiff.split(' ')[0])
            dtPub = dtNow - relativedelta(minutes=d)
        elif 'seconds ago' in dtDiff:
            dtPub = dtNow
        else:
            dtPub = dtNow
        return dtPub

