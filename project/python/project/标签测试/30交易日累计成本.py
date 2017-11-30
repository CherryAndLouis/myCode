import pymysql
from functools import reduce
from project.util.dateUtil import dateUtil
from project.util.log import Log
#定义验证的资产账户
fund_account="570000099"

#连接结果数据库
db_louis=pymysql.connect(host='10.20.18.174', port=3306, user='root', passwd='Hundsun123',db='louis')
获取游标1=db_louis.cursor()
#连接原始华安数据库
db_huaan=pymysql.connect(host='10.20.18.174', port=3306, user='root', passwd='Hundsun123',db='huaan')
获取游标2=db_huaan.cursor()
#查询结果数据sql
结果="SELECT * FROM tradingdaycumulativecost_out where  fund_account="+fund_account
#查询总资产sql
查询his_asset资产sql="SELECT fund_account,init_date,total_asset FROM huaan.his_asset where  fund_account="+fund_account
#保存查询的结果
获取游标1.execute(结果)
近30交易日累计成本=获取游标1.fetchall()
#总资产结果
获取游标2.execute(查询his_asset资产sql)
总资产=获取游标2.fetchall()

#累加求和
def 相加求和 (L):
    def 相加(x,y):
        return x+y
    return reduce(相加,L)

#获取期初日成本
def 期初成本(期初日期):
    上一个交易日=dateUtil().getLastDay(期初日期)
    上个交易日总资产sql="select total_asset from his_asset where fund_account="+fund_account+" and init_date="+上一个交易日
    获取游标2.execute(上个交易日总资产sql)
    A=获取游标2.fetchall()
    if len(A) == 0:
        today_assetsql="select total_asset from his_asset where fund_account="+fund_account+" and init_date="+期初日期
        获取游标2.execute(today_assetsql)
        today_asset=获取游标2.fetchall()
        if len(today_asset) == 0:
            return 0
        else:
            return today_asset[0][0]
    else:
        资产值=A[0][0]
        资金流水="select total_in from  foundjour where fund_account="+fund_account+" and init_date="+期初日期
        获取游标1.execute(资金流水)
        净流入 =获取游标1.fetchall()
        if len(净流入) == 0:
            return  资产值
        else:
            return 资产值+净流入[0][0]

存放数据=[]
for x in 近30交易日累计成本:
    init_date=x[2]
    结果数据=x[1]
    前30个交易日列表=dateUtil().getLastNDaysList(init_date,29)
    期初日期=前30个交易日列表[0]
    当天成本=[]
    if init_date <20160714:
        first_datesql = "select total_asset from his_asset where fund_account=" + fund_account + " and init_date=" + "20160601"
        获取游标2.execute(first_datesql)
        first_date = 获取游标2.fetchall()
        first_date_asset=first_date[0][0]
        当天成本 = [first_date_asset, ]
        to_daysql="select init_date from his_asset where fund_account=" + fund_account + " and init_date<=" + str(init_date)+" order by init_date"
        获取游标2.execute(to_daysql)
        to_daylist = 获取游标2.fetchall()
        for b in to_daylist[1:]:
            date_1=b[0]
            资金流水 = "select total_in from  foundjour where fund_account=" + fund_account + " and init_date=" + str(date_1)
            获取游标1.execute(资金流水)
            净流入 = 获取游标1.fetchall()
            if len(净流入)==0:
                当天成本.append(当天成本[-1])
            else:
                当天成本.append(当天成本[-1]+净流入[0][0])
    else:
        期初日成本 = 期初成本(期初日期)
        当天成本 = [期初日成本,]
        for a in 前30个交易日列表[1:]:
            资金流水 = "select total_in from  foundjour where fund_account=" + fund_account + " and init_date=" + a
            获取游标1.execute(资金流水)
            净流入 = 获取游标1.fetchall()
            if len(净流入)==0:
                当天成本.append(当天成本[-1])
            else:
                当天成本.append(当天成本[-1]+净流入[0][0])
    计算结果=相加求和(当天成本)
    if 计算结果 == 结果数据:
        print('验证通过',init_date,'表结果',结果数据)
    else:
        print('验证不通过',init_date,'计算结果：',计算结果,'表结果',结果数据)








