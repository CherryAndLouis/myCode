import pymysql
from util.dateUtil import dateUtil

#验证的账号
fund_account="120012034";

#数据库配置
db_louis=pymysql.connect(host='10.20.18.174', port=3306, user='root', passwd='Hundsun123',db='louis',use_unicode=True, charset="utf8");
connection_louis=db_louis.cursor();
db_huaan=pymysql.connect(host='10.20.18.174', port=3306, user='root', passwd='Hundsun123',db='huaan',use_unicode=True, charset="utf8");
connection_huaan=db_huaan.cursor();

#查询结果数据
resultsql = "select * from stockdayprofit where fund_account = "+fund_account;
connection_louis.execute(resultsql);
resultlist = connection_louis.fetchall();

for x in resultlist:

    #查询今日股票市值
    stock_market_todaysql="select current_amount,correct_amount,last_price from datastockextend where fund_account = "+fund_account+" and init_date = "+str(x[2]);
    connection_louis.execute(stock_market_todaysql);
    stock_market_todaylist = connection_louis.fetchall();
    total_market_today = 0;
    if len(stock_market_todaylist) == 0:
        print("没有持仓数据"+x[2])
    else:
        for a in stock_market_todaylist:
           stock_market = (a[0]+a[1]) * a[2];
           total_market_today = total_market_today+stock_market;
    lastday=dateUtil().getLastDay(x[2]);

    #查询上个交易日股票市值
    stock_market_lastdaysql = "select current_amount,correct_amount,last_price from datastockextend where fund_account = " + fund_account + " and init_date = " +lastday;
    connection_louis.execute(stock_market_lastdaysql);
    stock_market_lastdaylist = connection_louis.fetchall();
    total_market_lastday = 0;
    if len(stock_market_lastdaylist) == 0:
        print("没有持仓数据"+x[2])
    else:
        for a in stock_market_lastdaylist:
           stock_market = (a[0]+a[1]) * a[2];
           total_market_lastday = total_market_lastday+stock_market;

    #查询一共费用
    faresql = "select sum(fare0+fare1+fare2+fare3+farex) from his_deliver where fund_account = "+fund_account+" and init_date = "+str(x[2]);
    connection_huaan.execute(faresql);
    farelist = connection_huaan.fetchall();
    fare=0
    if farelist[0][0] == None:
        fare = 0;
    else :
        fare = farelist[0][0];
    #今日卖出
    sell_balancesql = "select sum(business_balance) from his_deliver where business_flag in (4001) and exchange_type in('1','2') and money_type = '0' and fund_account = "+fund_account+" and init_date = "+str(x[2]);
    sell_balance = 0;
    connection_huaan.execute(sell_balancesql);
    sell_balancelist = connection_huaan.fetchall();
    if sell_balancelist[0][0] ==None:
        sell_balance = 0;
    else:
        sell_balance = sell_balancelist[0][0];
    #今日买入
    buy_balancesql = "select sum(business_balance) from his_deliver where business_flag in (4002) and exchange_type in('1','2') and money_type = '0' and fund_account = "+fund_account+" and init_date = "+str(x[2]);
    buy_balance = 0;
    connection_huaan.execute(buy_balancesql);
    buy_balancelist = connection_huaan.fetchall();
    if buy_balancelist[0][0]==None:
        buy_balance = 0;
    else:
        buy_balance = buy_balancelist[0][0];
    #股息
    dividendsql = "select sum(business_balance) from his_deliver where business_type = '6' and exchange_type in('1','2') and money_type = '0' and fund_account = "+fund_account+" and init_date = "+str(x[2]);
    dividend = 0;
    connection_huaan.execute(dividendsql);
    dividendlist = connection_huaan.fetchall();
    if dividendlist[0][0]==None:
        dividend = 0;
    else:
        dividend = dividendlist[0][0];
    #配股入账
    allotmentsql = "select sum(business_amount * business_price) from his_deliver where business_type = '2' and exchange_type in('1','2') and money_type = '0' and fund_account = "+fund_account+" and init_date = "+str(x[2]);
    allotment = 0;
    connection_huaan.execute(allotmentsql);
    allotmentlist = connection_huaan.fetchall();
    if allotmentlist[0][0]==None:
        allotment = 0;
    else:
        allotment = allotmentlist[0][0];
    #新股入账
    newsharessql = "select sum(business_amount * business_price) from his_deliver where business_type = '4' and exchange_type in('1','2') and money_type = '0' and fund_account = "+fund_account+" and init_date = "+str(x[2]);
    newshares = 0;
    connection_huaan.execute(newsharessql);
    newshareslist = connection_huaan.fetchall();
    if newshareslist[0][0] == None:
        newshares = 0;
    else:
        newshares = newshareslist[0][0];
    #托管转入
    escrowintosql = "select sum(business_amount * business_price) from his_deliver where business_type = '7' and business_flag = '4009' and exchange_type in('1','2','9') and money_type = '0' and fund_account = "+fund_account+" and init_date = "+str(x[2]);
    escrowinto = 0;
    connection_huaan.execute(escrowintosql);
    escrowintolist = connection_huaan.fetchall();
    if escrowintolist[0][0] == None:
        escrowinto = 0;
    else:
        escrowinto = escrowintolist[0][0];
    #托管转出
    escrowoutsql = "select sum(business_amount * business_price) from his_deliver where business_type = '7' and business_flag = '40010' and exchange_type in('1','2','9') and money_type = '0' and fund_account = " + fund_account + " and init_date = " + str(x[2]);
    escrowout = 0;
    connection_huaan.execute(escrowoutsql);
    escrowoutlist = connection_huaan.fetchall();
    if escrowoutlist[0][0] == None:
        escrowout = 0;
    else:
        escrowout = escrowoutlist[0][0];
    #转托转入
    transferintosql = "select sum(business_amount * business_price) from his_deliver where business_type = '8' and business_flag = '4007' and exchange_type in('1','2','9') and money_type = '0' and fund_account = " + fund_account + " and init_date = " + str(x[2]);
    transferinto = 0;
    connection_huaan.execute(transferintosql);
    transferintolist = connection_huaan.fetchall();
    if transferintolist[0][0] == None:
        transferinto = 0;
    else:
        transferinto = transferintolist[0][0];
    #转托转出
    transferoutsql = "select sum(business_amount * business_price) from his_deliver where business_type = '8' and business_flag = '4007' and exchange_type in('1','2','9') and money_type = '0' and fund_account = " + fund_account + " and init_date = " + str(x[2]);
    transferout = 0;
    connection_huaan.execute(transferoutsql);
    transferoutlist = connection_huaan.fetchall();
    if transferoutlist[0][0] == None:
        transferout = 0;
    else:
        transferout = transferoutlist[0][0];
    #股息红利税补缴
    bonussql = "select sum(business_balance) from his_deliver where business_flag = '2434' and exchange_type in('1','2','9') and money_type = '0' and fund_account = " + fund_account + " and init_date = " + str(x[2]);
    bonus = 0;
    connection_huaan.execute(bonussql);
    bonuslist = connection_huaan.fetchall();
    if bonuslist[0][0] == None:
        bonus = 0;
    else:
        bonus = bonuslist[0][0];
    #对比数据
    calculate = total_market_today-total_market_lastday+sell_balance-buy_balance-fare+dividend-allotment-newshares-escrowinto+escrowout-transferinto+transferout-bonus;
    calculate = round(calculate,2)
    if calculate == x[1]:
        print("测试通过",x[2]);
    else :
        print("测试不通过",x[2],"计算结果为：",calculate,"数据库结果为：",x[1]);