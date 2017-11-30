import sys
class openFile():

    # 获取closeDate中的日期
    def getCloseDate(self,filePath):
        #readlines()带有\n
        dateList = [line.rstrip() for line in open(filePath).readlines()]
        return dateList
