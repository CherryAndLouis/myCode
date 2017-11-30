import pymysql
from util.log import Log
from util.dateUtil import dateUtil


#输出日志
log = Log().getLogger()
#计算日期
initDate = 20170531
期末日期 = str(initDate)
baseDate = dateUtil()
基准期初日期 = baseDate.get基准期初日期(initDate)

connOrg = pymysql.connect(host='10.20.18.174', port=3306, user='root', passwd='Hundsun123',db='huaan')
curOrg = connOrg.cursor()

connRes = pymysql.connect(host='10.20.18.174', port=3306, user='root', passwd='Hundsun123',db='fanresult')
curRes = connRes.cursor()

resSql = "select fund_account,stock_code,income_balance from userstockincome"
curRes.execute(resSql)
resultDataList = curRes.fetchall()
if len(resultDataList) == 0 :
    log.info("数据表userstockincome无数据，无法进行测试对比")
else:
    for resultData in resultDataList:
        今日股票市值sql = "select sum((current_amount + correct_amount) * last_price) from his_datastock, his_price " \
                    + " where fund_account = " + str(resultData[0]) + " and his_datastock.money_type = '0' and his_datastock.init_date = " \
                    + 期末日期 + " and his_datastock.stock_code = " + str(resultData[1]) + " and his_datastock.init_date = his_price.init_date " \
                    + " and his_datastock.stock_code = his_price.stock_code"

        curOrg.execute(今日股票市值sql)
        今日股票市值 = curOrg.fetchall()
        if len(今日股票市值) == 0 :
            今日股票市值 = float(今日股票市值[0][0])
        else:
            今日股票市值 = 0.0

        去年今日股票市值sql = "select sum((current_amount + correct_amount) * last_price) from his_datastock, his_price " \
                      + " where fund_account = " + str(resultData[0]) + " and his_datastock.money_type = '0' and his_datastock.init_date = " \
                      + 基准期初日期[0] + " and his_datastock.stock_code = " + str(resultData[1]) + " and his_datastock.init_date = his_price.init_date " \
                      + " and his_datastock.stock_code = his_price.stock_code"
        curOrg.execute(去年今日股票市值sql)
        去年今日股票市值 = curOrg.fetchall()
        if len(去年今日股票市值) == 0:
            去年今日股票市值 = float(去年今日股票市值[0][0])
        else:
            去年今日股票市值 = 0.0

        今年股票卖出金额sql = " select sum(business_balance) from his_deliver where fund_account = " \
                      + str(resultData[0]) + " and money_type = '0' and init_date >= " + 基准期初日期[1] \
                      + " and init_date <= " + 期末日期 + " and stock_code = " + str(resultData[1]) + " and business_flag in(4001) " \
                      + " and exchange_type in('1','2')"
        curOrg.execute(今年股票卖出金额sql)
        今年股票卖出金额 = curOrg.fetchall()
        if len(今年股票卖出金额) == 0:
            今年股票卖出金额 = float(今年股票卖出金额[0][0])
        else:
            今年股票卖出金额 = 0.0


        今年股票买入金额sql = "select sum(business_balance) from his_deliver where fund_account = " \
                      + str(resultData[0]) + " and money_type = '0' and init_date >= " + 基准期初日期[1] \
                      + " and init_date <= " + 期末日期 + " and stock_code = " + str(resultData[1]) \
                      + " and business_flag in(4002) and exchange_type in('1','2')"
        curOrg.execute(今年股票买入金额sql)
        今年股票买入金额 = curOrg.fetchall()
        if len(今年股票买入金额) == 0:
            今年股票买入金额 = float(今年股票买入金额[0][0])
        else:
            今年股票买入金额 = 0.0


        今年股票交易手续费sql = "select sum(fare0+fare1+fare2+fare3+farex) from his_deliver where fund_account = " \
                       + str(resultData[0]) + " and money_type = '0' and init_date >= " + 基准期初日期[1] \
                       + " and init_date <= " + 期末日期 + " and stock_code = " + str(resultData[1]) \
                       + " and business_flag in(4001,4002) and exchange_type in('1','2')"
        curOrg.execute(今年股票交易手续费sql)
        今年股票交易手续费 = curOrg.fetchall()
        if len(今年股票交易手续费) == 0:
            今年股票交易手续费 = float(今年股票交易手续费[0][0])
        else:
            今年股票交易手续费 = 0.0


        股息入账sql = "select sum(business_balance) from his_deliver where fund_account = " + str(resultData[0]) \
                  + " and money_type = '0'  and init_date >= " + 基准期初日期[1] + " and init_date <= " + 期末日期 \
                  + " and stock_code = " + str(resultData[1]) + " and business_type = '6' and exchange_type in('1','2')"

        curOrg.execute(股息入账sql)
        股息入账 = curOrg.fetchall()
        if len(股息入账) == 0:
            股息入账 = float(股息入账[0][0])
        else:
            股息入账 = 0.0


        配股入账sql = "select sum(business_amount * business_price) from his_deliver where fund_account = " \
                  + str(resultData[0]) + " and money_type = '0' and init_date >= " + 基准期初日期[1] + " and init_date <= " + 期末日期 \
                  + " and stock_code = " + str(resultData[1]) + " and business_type = '2' and exchange_type in('1','2')"

        curOrg.execute(配股入账sql)
        配股入账 = curOrg.fetchall()
        if len(配股入账) == 0:
            配股入账 = float(配股入账[0][0])
        else:
            配股入账 = 0.0

        新股入账sql = "select sum(business_amount * business_price) from his_deliver where fund_account = " \
                  + str(resultData[0]) + " and money_type = '0' and init_date >= " + 基准期初日期[1] + " and init_date <= " + 期末日期 \
                  + " and stock_code = " + str(resultData[1]) + " and business_type = '4' and exchange_type in('1','2')"
        curOrg.execute(新股入账sql)
        新股入账 = curOrg.fetchall()
        if len(新股入账) == 0:
            新股入账 = float(新股入账[0][0])
        else:
            新股入账 = 0.0

        盈亏金额 = 今日股票市值 - 去年今日股票市值 + 今年股票卖出金额 - 今年股票买入金额 - 今年股票交易手续费 + 股息入账 - 配股入账 - 新股入账

        print(str(resultData[0]) + " " + str(resultData[1]) + " " + str(盈亏金额))


# 脚本文件 20160531  20170531
# ./run_import_job.py -f his_jobs.json -j ifs_hadoop_dev_deliver --init_date=20170531 --end_date=20170531
# ./run_import_job.py -f his_jobs.json -j ifs_hadoop_dev_price --init_date=20160801 --end_date=20170731
# ./run_import_job.py -f his_jobs.json -j ifs_hadoop_dev_dailyquote_jy --init_date=20170531 --end_date=20170531
# ./run_import_job.py -f his_jobs.json -j ifs_hadoop_dev_datastock --init_date=20170531 --end_date=20170531
# ./run_import_job.py -f his_jobs.json -j ifs_hadoop_dev_fundjour --init_date=20170531 --end_date=20170531

# ./mr_job.py -f mr_one_jobs.json -j datastockClean --init_date=20160531 --end_date=20170531



# ./mr_job.py -f mr_one_jobs.json -j hispriceClean --init_date=20160601 --end_date=20170531


# ./mr_job.py -f mr_two_jobs.json -j userstockincome --init_date=20170531 --end_date=20170531

# ./run_export_job.py -f export_jobs.json -j userstockincome --init_date=20170531 --end_date=20170531


