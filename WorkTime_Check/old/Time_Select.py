#coding=utf-8
import logging.config
import requests

logging.config.fileConfig(r'../Conf/debug.conf')
logs = logging.getLogger('TimeWork')

class Time_Select():
    def __init__(self):
        pass
    def Select_Time(self,se):
        print se
        self.se = se
        self.se.get("https://oa.kedacom.com/report/platform/console/main.do").text
        logs.debug("11111111")

    def post(self,url,data,head):
        return_data = self.se.post(url,data,head)
        return return_data

if __name__ =="__main__":
    #TS = Time_Select().Select_Time()
    a = 'test'
    s = a.split(' ')
    print s
