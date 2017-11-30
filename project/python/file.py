import pymysql
from functools import reduce
from project.util.dateUtil import dateUtil
from project.util.log import Log
前30个交易日列表=dateUtil().getLastNDaysList(20170321,29)
print(前30个交易日列表)