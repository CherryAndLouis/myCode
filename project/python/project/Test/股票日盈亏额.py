import pymysql
from util.dateUtil import dateUtil
from util.log import Log
#输出日志
log = Log().getLogger()
#结果数据库
connRes = pymysql.connect(host='10.253.0.56', port=3306, user='root', passwd='root',db='wei_test')
curRes = connRes.cursor()

#原始数据库
connOrg = pymysql.connect(host='10.253.0.56', port=3306, user='root', passwd='root',db='huaan')
curOrg = connOrg.cursor()

#结果数据内容
resSql = "select fund_account,init_date, income_balance from stockdayprofit limit 50"
curRes.execute(resSql)
quaryList = curRes.fetchall()


for quaryDate in quaryList:

    fd = str(quaryDate[0])
    initDate = str(quaryDate[1])
    incomeBalance = float(quaryDate[2])

    # 今日股票市值
    stockAmountSql = "SELECT sum(current_amount * last_price) FROM datastock, his_price "\
        + " WHERE fund_account = " + fd + " AND datastock.money_type = 0 "\
        + " AND his_price.money_type = 0 AND datastock.init_date = " + initDate\
        + " AND his_price.init_date =  " + initDate + " AND datastock.stock_code = his_price.stock_code"
    curOrg.execute(stockAmountSql)
    stockAmount = curOrg.fetchall()

    if stockAmount[0][0] != None:
        stockAmountNum = float(stockAmount[0][0])
    else:
        stockAmountNum = 0.0

    # 昨日股票市值
    lastDay = dateUtil().getLastDay(initDate)
    lastStockAmountSql = "SELECT sum(current_amount * last_price) FROM datastock, his_price "\
        + " WHERE fund_account = " + fd + " AND datastock.money_type = '0' "\
        + " AND his_price.money_type = '0' AND datastock.init_date = " + lastDay\
        + " AND his_price.init_date =  " + lastDay + " AND datastock.stock_code = his_price.stock_code"
    curOrg.execute(lastStockAmountSql)
    lastStockAmount = curOrg.fetchall()

    if lastStockAmount[0][0] != None:
        lastStockAmountNum = float(lastStockAmount[0][0])
    else:
        lastStockAmountNum = 0.0

    # 今日股票卖出金额
    stockSellAmountSql = "select sum(business_balance) from his_deliver where fund_account = " \
                      + fd + " and money_type = '0' and init_date = " + initDate\
                      + " and business_flag in(4001) and exchange_type in('1','2')"
    curOrg.execute(stockSellAmountSql)
    stockSellAmount = curOrg.fetchall()

    if stockSellAmount[0][0] != None:
        stockSellAmountNum = float(stockSellAmount[0][0])
    else:
        stockSellAmountNum = 0.0

    # 今日股票买入金额
    stockBuyAmountSql = "select sum(business_balance) from his_deliver where fund_account = " \
                      + fd + " and money_type = '0' and init_date = " + initDate\
                      + " and business_flag in(4002) and exchange_type in('1','2')"
    curOrg.execute(stockBuyAmountSql)
    stockBuyAmount = curOrg.fetchall()

    if stockBuyAmount[0][0] != None:
        stockBuyAmountNum = float(stockBuyAmount[0][0])
    else:
        stockBuyAmountNum = 0.0

    # 今日交易手续费
    fareAmountSql = "select sum(fare0) from his_deliver where fund_account = " + fd\
                + " and money_type = '0' and init_date = " + initDate + " and business_flag in(4001,4002)"\
                + " and exchange_type in('1','2')"
    curOrg.execute(fareAmountSql)
    fareAmount = curOrg.fetchall()

    if fareAmount[0][0] != None:
        fareAmountNum = float(fareAmount[0][0])
    else:
        fareAmountNum = 0.0

    # 股息入账
    getAmountSql = "select sum(business_balance) from his_deliver where fund_account = " + fd\
                + " and money_type = '0' and init_date = " + initDate + " and business_type = '6'"\
                + " and exchange_type in('1','2')"
    curOrg.execute(getAmountSql)
    getAmount = curOrg.fetchall()

    if getAmount[0][0] != None:
        getAmountNum = float(getAmount[0][0])
    else:
        getAmountNum = 0.0

    # 配股入账
    peiGuAmountSql = "select sum(business_amount * business_price) from his_deliver where fund_account = " + fd\
                + " and money_type = '0' and init_date = " + initDate + " and business_type = '2'" \
                + " and exchange_type in('1','2')"
    curOrg.execute(peiGuAmountSql)
    peiGuAmount = curOrg.fetchall()

    if peiGuAmount[0][0] != None:
        peiGuAmountNum = float(peiGuAmount[0][0])
    else:
        peiGuAmountNum = 0.0

    # 新股入账
    newStockAmountSql = "select sum(business_amount * business_price) from his_deliver where fund_account = "\
                + fd + " and money_type = '0' and init_date = " + initDate + " and business_type = '4'"\
                + " and exchange_type in('1','2')"

    curOrg.execute(newStockAmountSql)
    newStockAmount = curOrg.fetchall()

    if newStockAmount[0][0] != None:
        newStockAmountNum = float(newStockAmount[0][0])
    else:
        newStockAmountNum = 0.0

    # 计算结果
    resultNum = round(stockAmountNum - lastStockAmountNum + stockSellAmountNum - stockBuyAmountNum - fareAmountNum + getAmountNum\
                - peiGuAmountNum - newStockAmountNum,2)

    # print(str(stockAmountNum) +"," + str(lastStockAmountNum) + "," + str(stockSellAmountNum) + "," + str(stockBuyAmountNum)\
    #       + "," + str(fareAmountNum) + "," + str(getAmountNum) +"," + str(peiGuAmountNum) + "," + str(newStockAmountNum))

    if resultNum == incomeBalance:
        log.info("账号：" + fd + " ,日期 " + initDate + " 的股票日盈亏额测试通过")
    else:
        log.info("账号：" + fd + " ,日期 " + initDate + " 的股票日盈亏额测试不通过" + ",测试计算结果为 "\
              + str(resultNum) + " ,数据表结果为 " + str(incomeBalance))


curOrg.close()
curRes.close()
connOrg.close()
connRes.close()