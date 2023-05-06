from loginAPI import constructSession, login
from datetime import datetime
from datetime import timedelta
import time
import json



def getMonthlyData(inESIID):
    s = constructSession()
    todaysDate = datetime.today().strftime('%m/%d/%Y')
    oneYearAgo = (datetime.today() - timedelta(days = 365)).strftime('%m/%d/%Y')
    meterData = {
        "esiid": inESIID,
        "startDate": oneYearAgo,
        "endDate": todaysDate
    }
    r = s.post('https://www.smartmetertexas.com/api/usage/monthly', json=meterData)
    results = r.json()
    # print(results)
    usage = 0
    to_return = []
    for month in results['monthlyData']:
        to_print = month['startdate']
        to_print += " - "
        to_print += month['enddate']
        to_print += ": "
        to_print += str(month['actl_kwh_usg'])
        to_return.append(to_print)
        if month['actl_kwh_usg'] != None:
            usage += (month['actl_kwh_usg'])
    to_return.insert(0, str(usage))
    return to_return


if __name__ == '__main__':
    # getMonthlyData('ENTER ESIID HERE')
    pass