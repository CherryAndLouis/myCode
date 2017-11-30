import math

def get个股亏损得分(orgData1,orgData2,curRes,beginDate,endDate):

    # 计算结果存储在字典中
    resultScore = {}

    # 查询股票交易回合表stockholdcycle 和 stockholdcyclenotend
    sql1 = "select sell_balance, buy_balance, fare, end_date from stockholdcycle where fund_account = " \
            + orgData1 + " and stock_code = " + orgData2

    curRes.execute(sql1)
    quaryResult1 = curRes.fetchall()

    sql2 = "select sell_balance, buy_balance, fare, end_date from stockholdcyclenotend where fund_account = " \
            + orgData1 + " and stock_code = " + orgData2
    curRes.execute(sql2)
    quaryResult2 = curRes.fetchall()
    # 临时存放累加值
    tempSum = 0
    if quaryResult1 != None:

        for qR in quaryResult1:
            if (float(qR[0]) - float(qR[1]) - float(qR[2])) < 0 and int(qR[3]) > beginDate:

                if float(qR[1]) > 0:
                    tempSum += abs(float(qR[0]) - float(qR[1]) - float(qR[2])) / float(qR[1])

    if quaryResult2 != None:

        for qR in quaryResult2:
            if (float(qR[0]) - float(qR[1]) - float(qR[2])) < 0 and int(qR[3]) == endDate:

                if float(qR[1]) > 0:
                    tempSum += abs(float(qR[0]) - float(qR[1]) - float(qR[2])) / float(qR[1])

    if tempSum > 0:
        # resultSum = math.ceil(tempSum * 100)
        resultSum = tempSum * 100
    else:
        resultSum = -1  # 无计算结果

    resultScore[orgData1] = (orgData2, resultSum)

    return resultScore