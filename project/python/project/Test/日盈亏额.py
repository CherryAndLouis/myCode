import pymysql
from project.util import dateUtil
from project.util.log import Log
#输出日志
log = Log().getLogger()
#对比多少条数据
dateNum = "100"
#结果数据库
connRes = pymysql.connect(host='10.253.0.56', port=3306, user='root', passwd='root',db='wei_test')
curRes = connRes.cursor()
#原始数据库
connOrg = pymysql.connect(host='10.253.0.56', port=3306, user='root', passwd='root',db='huaan')
curOrg = connOrg.cursor()

resultSql = "select fund_account,init_date,income_balance from asset limit " + dateNum
curRes.execute(resultSql)
quaryList = curRes.fetchall()

for quaryData in quaryList:

    fd = str(quaryData[0])
    initDate = str(quaryData[1])
    tableResult = float(quaryData[2])
    # 今日资产
    todayAssetSql = "select total_asset from his_asset where fund_account = "\
                + fd + " and money_type = '0' and init_date = " + initDate
    curOrg.execute(todayAssetSql)
    todayAssetNum = curRes.fetchall()

    if len(todayAssetNum) != 0:
        todayAssetResult = float(todayAssetNum[0])
    else:
        todayAssetResult = 0.0

    # 昨日资产
    lastDate = dateUtil().getLastDay(initDate)
    lastDayAssetSql = "select total_asset from his_asset where fund_account = "\
                + fd + " and money_type = '0' and init_date = " + lastDate

    curOrg.execute(lastDayAssetSql)
    lastDayAssetNum = curRes.fetchall()

    if len(lastDayAssetNum) > 0:
        lastDayAssetResult = float(lastDayAssetNum[0])
    else:
        lastDayAssetResult = 0.0

    # 当日累计（银证转入）
    zhuanRuSql = "select sum(occur_balance) from his_banktransfer where fund_account = "\
                + fd + " and money_type = 0 and init_date = " + initDate \
                 + " and trans_type = '01' and bktrans_status = '2'"
    curOrg.execute(zhuanRuSql)
    zhuanRuNum = curRes.fetchall()

    if len(zhuanRuNum) > 0:
        lzhuanRuResult = float(zhuanRuNum[0][0])
    else:
        zhuanRuResult = 0.0
    # 当日累计（银证转出）
    zhuanChuSql =  "select sum(occur_balance) from his_banktransfer where fund_account = "\
                + fd + " and money_type = 0 and init_date = " + initDate \
                 + " and trans_type = '02' and bktrans_status = '2'"

    curOrg.execute(zhuanChuSql)
    zhuanChuNum = curRes.fetchall()
    if len(zhuanChuNum) > 0:
        zhuanChuResult = float(zhuanChuNum[0][0])
    else:
        zhuanChuResult = 0.0

    # 计算结果
    resultData = round(todayAssetResult - lastDayAssetResult - (zhuanRuResult - zhuanChuResult),2)

    if resultData == tableResult:
        log.info("账户：" + fd + " ,日期 " + initDate + " ,日盈亏额测试通过")
    else:
        log.info("账户：" + fd + " ,日期 " + initDate + " ,日盈亏额测试失败" + " ,测试计算结果为" + str(resultData)\
              + " ,表数据为 " + str(tableResult))
        # log.info(str(todayAssetResult) + " , " + str(lastDayAssetResult) + " , " + str(zhuanRuResult)\
        #       + " , " + str(zhuanChuResult))

curRes.close()
curOrg.close()
connOrg.close()
connRes.close()
