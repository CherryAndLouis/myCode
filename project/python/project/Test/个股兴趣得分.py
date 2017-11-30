from Test.个股盈利得分 import get个股盈利得分
from Test.个股亏损得分 import get个股亏损得分
from util.dateUtil import  dateUtil
import pymysql
import math
from util.log import Log
#输出日志
log = Log().getLogger()

#对比多少条数据
dateNum = "50"

#账户
fund_account = "100019187"

# 获得数据库链接
resultConn = pymysql.connect(host='10.253.0.56', port=3306, user='root', passwd='root',db='wei_test')
resConn = resultConn.cursor()
#获得计算结果的全部帐号和股票
sqlRes = "SELECT fund_account,stock_code,score FROM userstockinterestscore limit " + dateNum

#按照账户测试
# sqlRes = "SELECT fund_account,stock_code,score FROM userstockinterestscore where fund_account =  " + fund_account

resConn.execute(sqlRes)
orgDataList = resConn.fetchall()

#开始日期
endDate = 20170531
beginDate = int(dateUtil().getLastYearDay(str(endDate)))
#数据结果存放处
resultDate = {}

if orgDataList == None or len(orgDataList) == 0:
    log.info("开发数据未输入到相应的数据表！")
else:
    log.info("************************************************************************************")
    log.info("说明：'-1'代表该值无效,不会计入计算，如：个股盈利得分-1 ,个股亏损得分5；盈亏得分为 5 * 0.5 = 2.5 " \
          "如：个股盈利得分 6, 个股亏损得分-1；盈亏得分为 6 * 1 = 1")
    log.info("************************************************************************************")
    for orgData in orgDataList:

        # 个股当前持仓得分
        havingStocksql = "SELECT COUNT(*) FROM datastock WHERE fund_account = " + orgData[0]\
            + " AND init_date = " + str(endDate) + " AND current_amount > 0 AND stock_code = " + str(orgData[1])

        resConn.execute(havingStocksql)
        havingStock = resConn.fetchall()

        if havingStock != None and (int(havingStock[0][0])> 0):
            havingStockScore = 4
        else:
            havingStockScore = 0

        # 历史交易回合数
        cyclesql = "SELECT COUNT(*) FROM stockholdcycle where fund_account = " + orgData[0]\
            + " AND stock_code = " + orgData[1] + " AND end_date > " + str(beginDate)

        resConn.execute(cyclesql)
        cyclesqlNum = resConn.fetchall()

        cyclesqlNotEnd = "SELECT COUNT(*) FROM stockholdcyclenotend where fund_account = " + orgData[0]\
            + " AND stock_code = " + orgData[1] + " AND end_date = " + str(endDate)

        resConn.execute(cyclesqlNotEnd)
        cyclesqlNotEndNum = resConn.fetchall()

        cycleScore = 0
        if cyclesqlNum != None:
            cycleScore += int(cyclesqlNum[0][0])
        if cyclesqlNotEndNum != None:
            cycleScore += int(cyclesqlNotEndNum[0][0])

        # 持股周期分值
        holdsql = "select sum(stock_hold_cycle/5) from stockholdcycle where fund_account = "\
            + orgData[0] + " AND stock_code = " + orgData[1] + " AND end_date > " + str(beginDate)

        resConn.execute(holdsql)
        holdsqlcore = resConn.fetchall()

        holdsqlnoend = "select sum(stock_hold_cycle/5) from stockholdcyclenotend where fund_account = "\
            + orgData[0] + " AND stock_code = " + orgData[1] + " AND end_date = " + str(endDate)

        resConn.execute(holdsqlnoend)
        holdsqlnoendcore = resConn.fetchall()

        holdcyclescore = 0
        if holdsqlcore[0][0] != None:
            holdcyclescore += int(holdsqlcore[0][0])
        if holdsqlnoendcore[0][0] != None:
            holdcyclescore += int(holdsqlnoendcore[0][0])

        # 盈亏分值
        getMoneyDic = get个股盈利得分(orgData[0], orgData[1],resConn, beginDate, endDate)
        moneytScore = getMoneyDic[orgData[0]][1]

        # 亏损分值
        lostMoneyDic = get个股亏损得分(orgData[0], orgData[1], resConn, beginDate, endDate)
        lostScore = lostMoneyDic[orgData[0]][1]

        # 计算盈亏得分
        getLostScore = 0
        if moneytScore != -1:
            getLostScore += moneytScore
        if lostScore != -1 :
            getLostScore += lostScore*0.5

        resultScore = math.ceil(havingStockScore+ cycleScore + holdcyclescore/10 + getLostScore)

        #详细打印，调试使用

        if str(orgData[2]) == str(resultScore):
            log.info("账户" + orgData[0] + " ,股票" + str(orgData[1]) + " ,测试结果通过")
        else:
            log.info("账户" + orgData[0] + " ,股票" + str(orgData[1])+"，测试不通过"+ " ,测试计算分数为："\
                    + str(resultScore) + " ,数据表结果值为：" + str(orgData[2]))
            log.info("该账户的详细得分为----个股当前持仓得分：" + str(havingStockScore) + " ,历史交易回合得分" + str(cycleScore) \
              + " ,持股周期分值" + str(float(holdcyclescore)) + ",个股盈利得分" + str(moneytScore) \
              + " ,个股亏损得分" + str(lostScore))
        #存储结果
        resultDate[orgData[0]] = resultScore

resConn.close()
resultConn.close()