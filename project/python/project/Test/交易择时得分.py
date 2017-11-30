import pymysql
from util.dateUtil import dateUtil
from util.log import Log
#交易择时计算速度较慢，此处可以按照账户或者条数测试（通过resultQuarySql实现）

#账户
fund_account = "100019187"
#对比个数
limitNum = "100"

#输出日志
log = Log().getLogger()

#计算日期
initDate = 20170531

connRes = pymysql.connect(host='10.253.0.56', port=3306, user='root', passwd='root',db='wei_test')
curRes = connRes.cursor()

connOrg = pymysql.connect(host='10.253.0.56', port=3306, user='root', passwd='root',db='huaan')
curOrg = connOrg.cursor()

#按照条数测试
resultQuarySql = "select fund_account, score from accounttranstimingscore limit " + limitNum

#按照账户测试
# resultQuarySql = "select fund_account, score from accounttranstimingscore where fund_account = " + fund_account

curRes.execute(resultQuarySql)
quaryDataList = curRes.fetchall()

#交易择时结果存入字典
# tableResultList = {}
# for r in quaryDataList:
#     tableResultList[str(r[0])] = str(r[1])

#去年的日期
lastYearDay = dateUtil().getLastYearDay(initDate)
# 周平均
# 此处少算了一周，就是去年开始的那周,需要加进去
weekList = dateUtil().getWeekEndDay(initDate)
weekList.insert(0,lastYearDay)

#单次得分保存
scoreList = {}
#结果保存
resultScoreList = {}

for quaryData in quaryDataList:
    #账户
    fd = str(quaryData[0])

    #查询客户最近一年所有买入股票的记录
    buyStockSql = "select fund_account,init_date,stock_code,business_price from his_deliver where fund_account = "\
            + fd + " and money_type = '0' and init_date > " + lastYearDay + " and business_flag in(4002)"\
            + " and exchange_type in('1','2')"
    curOrg.execute(buyStockSql)
    buyStockList = curOrg.fetchall()

    # 计算每个庄账户的得分
    tempScoreList = []
    for buyData in buyStockList:
        # 每条买入记录计算得分
        tempDate = str(buyData[1])
        # try:
        for i in range(1, 12):
            # 每次循环往后延长一天
            tempDate = dateUtil().getNextDay(tempDate)

            hisPriceSql = "select closing_price,high_price from his_price where init_date = " \
                          + tempDate + " and stock_code = " + str(buyData[2])
            curOrg.execute(hisPriceSql)
            hisPriceResult = curOrg.fetchall()
            单笔得分 = 0
            #此时找不到下一个交易日的价格剔除掉
            if len(hisPriceResult) == 0:
                单笔得分 = -1
                break
            # 找到下一个交易日的价格
            if (float(hisPriceResult[0][0]) > float(buyData[3]) * 1.01) or (
                        float(hisPriceResult[0][1]) > float(buyData[3]) * 1.02):
                单笔得分 = 100 - (i - 1) * 10
                break
        # except ValueError:

        #保存每只股票的单次得分,找不到下一个交易日价格的股票剔除掉
        if 单笔得分 != -1:
            tempScoreList.append([str(buyData[1]),str(buyData[2]),单笔得分])
        else:
            log.info(fd + "存在未计算出得分，剔除掉的情况,日期为" + str(buyData[1]) + ",股票为：" + str(buyData[2]))
    #每个账户存入一个字典
    scoreList[fd] = tempScoreList

    # 计算周得分
    weekResultScoreList = {}
    eachWeekScore = []
    for index in range(len(weekList)-1):
        # 上一周和本周的结尾
        begin = int(weekList[index])
        end = int(weekList[index+1])

        #循环每一条数据
        weekSum = 0
        weekNum = 0
        for eachScore in tempScoreList:
            #得到每条数据的日期
            buyDataTemp = int(eachScore[0])
            if buyDataTemp > begin and buyDataTemp <= end:
                weekNum += 1
                weekSum += int(eachScore[2])
                log.info("（" +str(begin) + "----" + str(end)+ "]之间存在的交易：" + "帐号：" + \
                      fd + " 日期：" + str(buyDataTemp) + " ,股票为：" + str(eachScore[1]) + " ,得分为：" + str(eachScore[2]))
        # 如果本周有数据
        if weekNum > 0:
            eachWeekScore.append(float(weekSum/weekNum))

    testScore = round(sum(eachWeekScore) / len(eachWeekScore))
    tableScore = int(str(quaryData[1]))
    if testScore == tableScore:
        log.info("账户：" + fd + " ,的得分为：" + str(testScore) + " ,测试结果与数据表结果一致，测试通过！")

    else:
        log.info("账户：" + fd + ",的测试得分为：" + str(testScore) + " ,数据表分数为：" + str(tableScore) +" ,测试结果与数据表结果不一致，测试失败！,测试计算周数据详情如下：")
        log.info("周得分详情：" + str(eachWeekScore))

curOrg.close()
curRes.close()
connOrg.close()
connRes.close()