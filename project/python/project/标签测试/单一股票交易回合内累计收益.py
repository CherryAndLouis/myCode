import pymysql
from functools import reduce
#验证账号
fund_account="100019187"


#数据库连接信息
db_chenk=pymysql.connect(host='10.20.18.174', port=3306, user='root', passwd='Hundsun123',db='chenk')
connection_chenk=db_chenk.cursor()
db_louis=pymysql.connect(host='10.20.18.174', port=3306, user='root', passwd='Hundsun123',db='louis')
connection_louis=db_louis.cursor()

#查询已清仓股票代码
stockholdsql="select stock_code,buy_balance,sell_balance,fare,begin_date,end_date from stockholdcycle where fund_account="+ fund_account
#已清仓股票代码列表
connection_chenk.execute(stockholdsql)
stockholdlist=connection_chenk.fetchall()

for x in stockholdlist:
    stockcode=x[0]
    profit=x[2]-x[1]-x[3]
    begindate=x[4]
    enddate=x[5]
    #查询结果数据
    resultsql="select * from stock_hold_cycle_income where fund_account="+fund_account+" and stock_code="+stockcode+" and begin_date= "+begindate+" and end_date="+enddate
    connection_louis.execute(resultsql)
    resultlist=connection_louis.fetchall()
    for a in resultlist:
        result_profit=a[2]
        if result_profit == profit:
            print("测试通过",profit)
        else:
            print("测试不通过，已清仓，计算结果",profit,"标签结果",result_profit,"股票代码",x[0],"账号",fund_account)

#查询未清仓股票代码
stockholdnotendsql="select stock_code,buy_balance,sell_balance,fare,begin_date,end_date  from stockholdcyclenotend where fund_account="+ fund_account
#未清仓股票代码列表
connection_chenk.execute(stockholdnotendsql)
stockholdnotendlist=connection_chenk.fetchall()
for z in stockholdnotendlist:
    stock_code_notend=z[0]
    #查询持仓
    datastocksql="select current_amount,correct_amount,last_price from datastockextend where fund_account="+fund_account+" and stock_code="+stock_code_notend+" and init_date="+"20170531"
    connection_louis.execute(datastocksql)
    datastocklist=connection_louis.fetchall()
    profit_notend=(datastocklist[0][0]+datastocklist[0][1])*datastocklist[0][2]+z[2]-z[1]-z[3]
    # 查询结果数据
    result_notendsql = "select * from stock_hold_cycle_income where fund_account=" + fund_account + " and stock_code=" + z[0] + " and begin_date= " + z[4] + " and end_date=" + z[5]
    connection_louis.execute(result_notendsql)
    resultnotendlist = connection_louis.fetchall()
    for a in resultnotendlist:
        result_profit = a[2]
        if result_profit == profit_notend:
            print("测试通过",profit_notend)
        else:
            print("测试不通过，未清仓，计算结果",profit_notend,"标签结果",result_profit,"股票代码",z[0],"账号",fund_account)