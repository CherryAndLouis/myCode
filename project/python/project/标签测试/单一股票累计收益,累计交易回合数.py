import pymysql
from functools import reduce
#验证账号
fund_account="100019187"
#连接数据库
db_louis=pymysql.connect(host='10.20.18.174', port=3306, user='root', passwd='Hundsun123',db='louis')
connection_louis=db_louis.cursor()
db_chenk=pymysql.connect(host='10.20.18.174', port=3306, user='root', passwd='Hundsun123',db='chenk')
connection_chenk=db_chenk.cursor()