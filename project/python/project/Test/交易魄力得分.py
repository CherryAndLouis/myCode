import pymysql
import math
from util import dateUtil
from util.log import Log

#对比多少条数据
dateNum = "50"

#输出日志
log = Log().getLogger()

# 根据讨论结果，两次向上取整
# 用于取原始的asset表
# orginConn = pymysql.connect(host='10.253.0.56', port=3306, user='root', passwd='root',db='huaan')
# curOrg = orginConn.cursor()
# 用于取原始的asset表
resultConn = pymysql.connect(host='10.253.0.56', port=3306, user='root', passwd='root',db='wei_test')
curRes = resultConn.cursor()

# 周日期
# dateList = [20160603,20160608,20160617,20160624,20160701,20160708,20160715,20160722,20160729,20160805,20160812,20160819,20160826,20160902,20160909,20160914,20160923,20160930,20161014,20161021,20161028,20161104,20161111,20161118,20161125,20161202,20161209,20161216,20161223,20161230,20170106,20170113,20170120,20170126,20170203,20170210,20170217,20170224,20170303,20170310,20170317,20170324,20170331,20170407,20170414,20170421,20170428,20170505,20170512,20170519,20170526,20170531]
dateList = dateUtil.dateUtil().getWeekEndDay("20170531")

#获取交易魄力得分表中的证券账户
sqlRes = "SELECT fund_account,score FROM accounttransboldnessscore limit " + dateNum
curRes.execute(sqlRes)
fundAcountList = curRes.fetchall()

#计算结果存储在字典中
resultScore = {}

for fundAcount in fundAcountList:
    #计算有数据的周数
    missNum = 0
    总得分 = 0
    得分 = 0
    for selectDate in dateList:
        # 目前的数据表中该数据为1，此处先默认为1
        周股票仓位 = 1
        #获得fundacount，selectDate的周收益率
        sqlYeild = "SELECT week_yield FROM weekyield where init_date = " + str(selectDate)\
                   + " and fund_account = " + fundAcount[0]
        curRes.execute(sqlYeild)

        #防止查找结果为None
        temp = curRes.fetchone()

        if temp == None:
            #记录None的个数
            missNum += 1
            #跳出循环
            continue
        #周收益率
        周收益率 = float(temp[0])

        # 获得selectDate沪深300涨跌比率
        sqlhs300 = "SELECT week_ratio FROM hs300 where init_date = " + str(selectDate)
        curRes.execute(sqlhs300)
        # 沪深300涨跌幅
        沪深300周涨跌比率 = float(curRes.fetchone()[0])

        #计算公式
        if 沪深300周涨跌比率 > 0:
            if 周收益率 > 沪深300周涨跌比率:
                if 周股票仓位 >= 0.8:
                    得分 = 80 + math.ceil((周股票仓位*100-0.8*100))
                elif 周股票仓位 >= 0.5:
                    得分 = 50 + math.ceil((周股票仓位*100-0.5*100))
                elif 周股票仓位 >= 0.3:
                    得分 = 30 + math.ceil((周股票仓位*100-0.3*100))
                else:
                    得分 = math.ceil(周股票仓位*100)
            else:
                if 周股票仓位 >= 0.8:
                    得分 = 40 + math.ceil((周股票仓位*100-0.8*100) *(-1))
                elif 周股票仓位 >= 0.5:
                    得分 = 65 + math.ceil((周股票仓位*100-0.5*100) *(-0.5))
                elif 周股票仓位 >= 0.3:
                    得分 = 75 + math.ceil((周股票仓位*100-0.3*100) *(-0.5))
                else:
                    得分 = 75 + math.ceil((0.3*100-周股票仓位*100) *(0.5))
        elif 沪深300周涨跌比率 >= -0.01:
            if 周股票仓位 >= 0.8:
                得分 = 40 + math.ceil((周股票仓位*100-0.8*100) *(-0.5))
            elif 周股票仓位 >= 0.5:
                得分 = 55 + math.ceil((周股票仓位*100-0.5*100)*(-0.5))
            elif 周股票仓位 >= 0.2:
                得分 = 70 + math.ceil((周股票仓位*100-0.2*100)*(-0.5))
            else:
                得分 = 70 + math.ceil((0.2*100-周股票仓位*100)*(0.5))
        else:
            if 周股票仓位 >= 0.8:
                得分 = 10 + math.ceil((周股票仓位*100-0.8*100) *(-0.5))
            elif 周股票仓位 >= 0.5:
                得分 = 40 + math.ceil((周股票仓位*100-0.5*100) *(-1))
            elif 周股票仓位 >= 0.2:
                得分 = 70 + math.ceil((周股票仓位*100-0.2*100)*(-1))
            else:
                得分 = 70 + math.ceil((0.2*100-周股票仓位*100)*(1.5))
        总得分 += 得分
        #打印详细数据信息
        # 调试输出
        # log.info("账户 " + fundAcount[0]+ " ,日期" + str(selectDate)\
        #       + " ,周收益率" + str(周收益率) + " ,沪深300周涨跌比率" + str(沪深300周涨跌比率) \
        #       + " ,仓位 1" +" ,得分" + str(得分))
    #计算平均值
    有数据的周数 = len(dateList)-missNum
    if 有数据的周数 > 0:
        平均得分 = 总得分/有数据的周数
    else:
        平均得分 = -1
    resultScore[fundAcount[0]] = round(平均得分,2)
    # 输出结果
    #调试输出
    # log.info("账户为" + fundAcount[0] + "-测试计算结果：" + str(round(平均得分,2))\
    #       + " ,数据表中结果：" + str(fundAcount[1]) + " ,有数据的周数" + str(有数据的周数) + " ,总得分" + str(总得分))

    # 比较结果，输出内容
    ll = str(round(平均得分, 2))
    if len(ll) == 4:
        ll += "0"

    if ll == str(fundAcount[1]):
        log.info("账户为" + fundAcount[0] + " ,经与数据表结果比对，测试结果通过")
    else:
        log.info("账户为" + fundAcount[0] + " ,测试不通过"+" ,测试计算结果：" + str(round(平均得分, 2))\
                 + "数据表结果值为：" + str(fundAcount[1]))
# curOrg.close()
curRes.close()
# orginConn.close()
resultConn.close()