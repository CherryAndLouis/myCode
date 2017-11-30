import pymysql
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
resSql = "select fund_account,init_date, daily_buying_of_securities from hisdeliver"
curRes.execute(resSql)
quaryList = curRes.fetchall()

for quaryData in quaryList:

    fd = str(quaryData[0])
    initDate = str(quaryData[1])
    orgSql = "select sum(business_balance) from his_deliver where fund_account = "\
        + fd + " and money_type = '0' and init_date = " + initDate + " and business_flag in(4002) "\
             + " and exchange_type in('1','2')"

    curOrg.execute(orgSql)
    resultSum = curOrg.fetchall()

    resultValue = 0.00
    if resultSum[0][0] != None:
        resultValue = round(float(resultSum[0][0]),2)

    if resultValue == float(quaryData[2]):
        log.info("帐号：" + fd + " ,日期 " + initDate + " ,经比较测试通过")
    else:
        log.info("帐号：" + fd + " ,日期 " + initDate +" ,经比较测试失败，测试计算结果为："\
                 + str(resultValue) + " ,数据表结果为：" + str(quaryData[2]))

curRes.close()
curOrg.close()
connRes.close()
connOrg.close()