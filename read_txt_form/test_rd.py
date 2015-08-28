from datetime import date
from dateutil.relativedelta import relativedelta
assert date(2016,1,1) == date(2015,12,1) + relativedelta(months=1) 
