import pymysql
from functools import reduce
#验证账号
fund_account="120020955"

#数据库连接信息
db_louis=pymysql.connect(host='10.20.18.174', port=3306, user='root', passwd='Hundsun123',db='louis')
connection_louis=db_louis.cursor()

#查询结果数据
result_sql="SELECT fund_account,income_balance,init_date from stock_income_balance where fund_account="+fund_account
connection_louis.execute(result_sql)
result_list=connection_louis.fetchall()

#相加函数
def calculate (L):
    def sum(x,y):
        return x+y
    return reduce(sum,L)

for x in result_list:
    init_date=x[2]
    income_balance=x[1]
    #查询每日盈亏
    every_profitsql="SELECT * from stockdayprofit where fund_account="+fund_account+" and init_date <="+str(init_date)
    connection_louis.execute(every_profitsql)
    every_profitlist=connection_louis.fetchall()
    calculate_result=[]
    if len(every_profitlist) == 0:
        calculate_result=[0,]
    else:
        for a in every_profitlist:
            income=a[1]
            calculate_result.append(income)
    result=calculate(calculate_result)
    #验证
    if result == income_balance:
        print('验证通过 日期：',int(init_date),'表结果',income_balance)
    else:
        print('验证不通过 日期：',int(init_date),'计算结果：',result,'表结果',income_balance)



