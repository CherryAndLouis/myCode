import pymysql
from util.dateUtil import dateUtil

#验证的账号
fund_account="570022331";

#数据库配置
db_louis=pymysql.connect(host='10.20.18.174', port=3306, user='root', passwd='Hundsun123',db='louis',use_unicode=True, charset="utf8");
connection_louis=db_louis.cursor();
db_huaan=pymysql.connect(host='10.20.18.174', port=3306, user='root', passwd='Hundsun123',db='huaan',use_unicode=True, charset="utf8");
connection_huaan=db_huaan.cursor();

#查询结果数据
resultsql = "select * from dayyield where fund_account = "+fund_account;
connection_louis.execute(resultsql);
resultlist = connection_louis.fetchall();
for x in resultlist:
    #查询日盈亏额
    day_profitsql = "select income_balance from asset where fund_account = "+fund_account+" and init_date = "+str(x[2]);
    connection_louis.execute(day_profitsql);
    day_profitlist = connection_louis.fetchall();
    day_profit = 0;
    if len(day_profitlist) == 0:
        day_profit = 0;
    else:
        day_profit = day_profitlist[0][0];
    #查询日成本
    day_costsql = "select total_asset from his_asset where fund_account = "+fund_account+" and init_date = "+str(x[2]);
    connection_huaan.execute(day_costsql);
    day_costlist = connection_huaan.fetchall();
    day_cost = 0;
    if len(day_profitlist) == 0 :
        print("今日总资产为空",x[2]);
    else:
        day_cost = day_costlist[0][0]-day_profit;
    #对比数据
    caculate = round(day_profit/day_cost,2);
    if caculate == x[1]:
        print("测试通过",x[2]);
    else :
        print("测试不通过",x[2],"计算结果为：",caculate,"表结果为：",x[1])