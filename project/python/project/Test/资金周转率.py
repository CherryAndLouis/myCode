import pymysql
from util.dateUtil import dateUtil
from util.log import Log
#输出日志
log = Log().getLogger()
#连接数据库,结果库
connRes = pymysql.connect(host='10.253.0.56', port=3306, user='root', passwd='root',db='wei_test')
curRes = connRes.cursor()

#连接数据库,原始库
connOrg = pymysql.connect(host='10.253.0.56', port=3306, user='root', passwd='root',db='huaan')
curOrg = connOrg.cursor()

#查询开发结果
resultSql = "SELECT fund_account,init_date,recent_year_turnover_rate_of_funds FROM assettrade limit 100"
curRes.execute(resultSql)
quaryResultList = curRes.fetchall()

resultList = {}
for quaryResult in quaryResultList:

    #帐号和日期
    fd = str(quaryResult[0])
    initD = str(quaryResult[1])

    #获得去年的日期
    lastYearInitD = dateUtil().getLastYearDay(initD)

    #得到近一年买入总额
    testSql = "select sum(business_balance) from his_deliver where fund_account = "\
              + fd + " and money_type = '0' and init_date > " + lastYearInitD

    curOrg.execute(testSql)
    testSumResult = curOrg.fetchall()

    # 得到成本（最近一年）
    costSql = "select year_cost from yearcost where fund_account = " + fd +" and init_date = " + initD
    curRes.execute(costSql)
    costResult = curRes.fetchall()
    resultRatio = 0.0000
    if len(costResult) != 0 and len(testSumResult) != 0 and testSumResult[0][0] != None:
        resultRatio = float(testSumResult[0][0])/float(costResult[0][0])

    resultRatio = round(resultRatio,4)

    resultList[fd] = [str(resultRatio),initD]

    if resultRatio == float(quaryResult[2]):
        log.info("帐号为：" + fd + " ,日期 " + initD + " ,经比较测试通过")
    else:
        log.info("帐号为：" + fd + " ,日期 " + initD + " ,经比较测试失败" \
                 +" ,测试计算结果为： " + str(resultRatio)+" ,数据表结果为：" + str(quaryResult[2]))

curOrg.close()
curRes.close()
connRes.close()
connOrg.close()






