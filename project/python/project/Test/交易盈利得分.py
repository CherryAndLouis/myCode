import pymysql
import math
from util import dateUtil
from util.log import Log

#输出日志
log = Log().getLogger()

#对比多少条数据
dateNum = "50"

# 链接数据库
conn = pymysql.connect(host='10.253.0.56', port=3306, user='root', passwd='root',db='wei_test')
cur = conn.cursor()

# 周日期
# 需要取一年内每周的最后一个交易日，对于end_date即使不是周末也是要算进去的
dateList = dateUtil.dateUtil().getWeekEndDay("20170531")

#获取交易盈利得分表中的证券账户
sqlScore = "SELECT fund_account, score FROM accounttransincomescore limit " + dateNum
cur.execute(sqlScore)
fundAcountList = cur.fetchall()
#计算结果存储在字典中
resultScore = {}
#循环账户
for fundacount in fundAcountList:
    #循环日期
    averageResult = 0
    missNum = 0
    for selectDate in dateList:
        resultweek = 0
        #获得fundacount，selectDate的周收益率
        sqlYeild = "SELECT week_yield FROM weekyield where init_date = " + str(selectDate)\
                   + " and fund_account = " + fundacount[0]
        cur.execute(sqlYeild)
        #防止查找结果为None
        temp = cur.fetchone()
        if temp == None:
            #记录None的个数
            missNum += 1
            #跳出循环
            continue
        #周收益率
        resultYeild = float(temp[0])

        # 获得selectDate沪深300涨跌比率
        sqlhs300 = "SELECT week_ratio FROM hs300 where init_date = " + str(selectDate)
        cur.execute(sqlhs300)
        #沪深300涨跌幅
        resultHs300 = float(cur.fetchone()[0])

        # 收益率计算公式
        if resultYeild >= 0:
            if resultYeild >= resultHs300:
                resultweek = math.ceil(60 + (resultYeild - resultHs300) / 0.005 * 2)
                if resultweek > 100:
                    resultweek = 100
            else:
                resultweek = math.floor(60 + (resultYeild - resultHs300)/0.01)
                if (resultweek < 40):
                    resultweek = 40
        else:
            if resultYeild >= resultHs300:
                resultweek = math.ceil(40 + (resultYeild - resultHs300)/0.01 *2)
                if resultweek > 60:
                    resultweek = 60
            else:
                resultweek = math.floor(40 + (resultYeild - resultHs300) / 0.005 * 2)
                if resultweek < 0:
                    resultweek = 0
        #累加
        averageResult += resultweek
        # 详细输出每周的数据
        # log.info("账户：" + str(fundacount[0]) + ",日期：" + str(selectDate) + ",本周收益率：" + str(resultYeild) \
        #   + ",hs300周涨跌幅：" + str(resultHs300) + ",周得分：" + str(resultweek))
    #计算平均值
    averageCount = len(dateList)-missNum
    if averageCount >0:
        averageResult = round(averageResult/(len(dateList)-missNum),2)
    else:
        averageResult = -1 # 无效值
    #结果存入字典resultScore
    resultScore[fundacount[0]] = averageResult

    #比较结果，输出内容
    ll = str(averageResult)
    if len(ll) == 4:
        ll += "0"

    if ll == str(fundacount[1]):
        log.info("帐号" + fundacount[0] + "经与数据表结果比对，测试结果通过")

    else:
        log.info("帐号" + fundacount[0] +"的测试计算结果为：" + str(averageResult) + "经对比测试不通过，数据表结果值为：" + str(fundacount[1]))

cur.close()
conn.close()

