# -*- coding:utf-8 -*-
import datetime
from project.util  import openFile


yearDays = 365
filePath = "E:\\公用文件\\project\\python\\project\\util\\close.txt"

class dateUtil():

    #获得每周的最后一个交易日,限定时间
    def getWeekEndDay(self,endDate):

        if type(endDate) == type(""):
            endDate = int(endDate)
        # 转换成日期
        tdate = datetime.datetime.strptime(str(endDate),"%Y%m%d")
        #计算开始时间
        beginDate = int((tdate - datetime.timedelta(days=yearDays)).strftime("%Y%m%d"))

        # 读取close.txt文件
        open = openFile.openFile()
        dateList = open.getCloseDate(filePath)

        # string转int
        listInt = [int(date) for date in dateList]

        # 筛选日期
        midDate = [x for x in listInt if x >= beginDate and x <= endDate]

        # 判断每周的最后一个交易日
        weekEndList = []
        #开始日期
        startDate = datetime.datetime.strptime(str(midDate[0]),"%Y%m%d")
        for d in midDate[1:]:
            tempDate = datetime.datetime.strptime(str(d),"%Y%m%d")
            shiftDay = (tempDate - startDate).days
            # 判断天数是否连续，将不连续的点存入序列
            if shiftDay == 1:
                startDate = tempDate
                # 可以使用yield改写成生成器，
                # if d == midDate[-1]:
                #     yield str(startDate.strftime("%Y%m%d"))
            else:
                # 可以使用yield改写成生成器，
                # yield str(startDate.strftime("%Y%m%d"))
                weekEndList.append(startDate.strftime("%Y%m%d"))
                startDate = tempDate

        #将最后日期也装入到日期中
        weekEndList.append(str(midDate[-1]))
        return weekEndList


    # 获得所有的交易日
    def getAllDay(self, endDate):

            if type(endDate) == type(""):
                endDate = int(endDate)
            # 转换成日期
            tdate = datetime.datetime.strptime(str(endDate), "%Y%m%d")
            # 计算开始时间
            beginDate = int((tdate - datetime.timedelta(days=yearDays)).strftime("%Y%m%d"))

            # 读取close.txt文件
            open = openFile.openFile()
            dateList = open.getCloseDate(filePath)

            # string转int
            listInt = [int(date) for date in dateList]

            # 筛选日期
            midDate = [x for x in listInt if x >= beginDate and x <= endDate]

            return midDate

    def getLastYearDay(self,strDate):
        # 转换成日期
        tdate = datetime.datetime.strptime(str(strDate), "%Y%m%d")
        # 计算去年的时间
        beginDate = (tdate - datetime.timedelta(days=yearDays)).strftime("%Y%m%d")
        return beginDate

    def get基准期初日期(self,strDate):
        # 转换成日期
        tdate = datetime.datetime.strptime(str(strDate), "%Y%m%d")
        # 计算去年的时间
        beginDate = (tdate - datetime.timedelta(days=yearDays)).strftime("%Y%m%d")
        # 读取close.txt文件
        open = openFile.openFile()
        dateList = open.getCloseDate(filePath)
        if  beginDate in dateList:
            期初 = dateList[dateList.index(beginDate)+1]
            return (beginDate,期初)
        else:
            tempdate = datetime.datetime.strptime(beginDate, "%Y%m%d")
            while True:
                tempdate = (tempdate - datetime.timedelta(days=1)).strftime("%Y%m%d")
                if tempdate in dateList:
                    期初 = dateList[dateList.index(tempdate) + 1]
                    return (tempdate,期初)
                else:
                    pass
                tempdate = datetime.datetime.strptime(tempdate, "%Y%m%d")

    # 得到上一个交易日
    def getLastDay(self,nowDate):
        # 读取close.txt文件
        open = openFile.openFile()
        dateList = open.getCloseDate(filePath)

        # string转int
        listInt = [int(date) for date in dateList]

        if type(nowDate) == type(""):
            tempDate = int(nowDate)
        else:
            tempDate = nowDate
        #如果是个交易日
        if tempDate in listInt:
            index = listInt.index(tempDate)
            return str(listInt[index-1])
        # 如果不是个交易日
        else:
            tempDate = datetime.datetime.strptime(str(nowDate), "%Y%m%d")
            while True:
                beginDate = int((tempDate - datetime.timedelta(days=1)).strftime("%Y%m%d"))
                tempDate = datetime.datetime.strptime(str(beginDate), "%Y%m%d")
                if beginDate in listInt:
                    return str(beginDate)

    # 得到下一个交易日
    def getNextDay(self,nowDate):
        # 读取close.txt文件
        open = openFile.openFile()
        dateList = open.getCloseDate(filePath)

        # string转int
        listInt = [int(date) for date in dateList]

        if type(nowDate) == type(""):
            tempDate = int(nowDate)
        else:
            tempDate = nowDate
        # 如果是个交易日
        if tempDate in listInt:
            index = listInt.index(tempDate)
            return str(listInt[index + 1])
        # 如果不是个交易日
        else:
            tempDate = datetime.datetime.strptime(str(nowDate), "%Y%m%d")
            while True:
                beginDate = int((tempDate + datetime.timedelta(days=1)).strftime("%Y%m%d"))
                if beginDate in listInt:
                    return str(beginDate)

    #判定当前日期属于年份的第几周，返回为“年份周数”
    def getWeekIndex(self,dateStr):
        tdate = datetime.datetime.strptime(str(dateStr), "%Y%m%d")
        weekIndex = tdate.isocalendar()
        return str(weekIndex[0]) + str(weekIndex[1])

    # 返回initDate往前推N个交易日的交易日列表，默认include = 0，包含自身
    def getLastNDaysList(self,initDate,n,include = 0):

        open = openFile.openFile()
        dateList = open.getCloseDate(filePath)
        initDate = str(initDate)

        index = dateList.index(initDate)
        if include == 0:
            return dateList[index-n:index+1]
        else:
            return dateList[index - n:index]

    # 返回initDate往后推N个交易日的交易日列表,默认include = 0，包含自身
    def getNextNDaysList(self, initDate, n,include = 0):

        open = openFile.openFile()
        dateList = open.getCloseDate(filePath)

        initDate = str(initDate)
        index = dateList.index(initDate)
        if include == 0:
            return dateList[index:index+n+1]
        else:
            return dateList[index:index+n]