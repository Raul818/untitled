from datetime import datetime, timedelta
import time
import datetime as dtm

months = (None, 'January', 'February', 'March', 'April','May','June', 'July', 'August', 'September', 'October', 'November', 'December')
for y in range(1, 13):
    m = months[y]
    dt = dtm.datetime(year=int(time.strftime("%Y")), month=y[1], day=1)
    enddate = int(time.mktime(dt.timetuple()))
    dt = dtm.datetime(year=int(time.strftime("%Y")), month=y[1], day=1) - dtm.timedelta(31)
    startdate = int(time.mktime(dt.timetuple()))