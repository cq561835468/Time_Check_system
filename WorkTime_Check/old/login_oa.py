#coding=utf-8
import re
import requests
import threading
import logging.config
import Pruduct_ini
import Time_Select
import json
import urllib

logging.config.fileConfig(r'../Conf/debug.conf')
logs = logging.getLogger('TimeWork')

class oa_time_to_work(threading.Thread):
    def __init__(self,Time,User,UserList):
        self.Time = Time
        # self.Begin_time = Begin_time
        self.User = User
        self.UserList = UserList
        self.se = requests.session()
        #----------------------------
        self.login_url = 'https://sso.kedacom.com:8443/CasServer/login'
        self.select1 = 'https://oa.kedacom.com/report-manager/ReportServer?_=1531295170097&op=fr_form&cmd=form_getsource&sessionID=5402&__widgetname__=%5B5b%5D%22USERID%22%5B5d%5D'
        self.select2 = 'https://oa.kedacom.com/report-manager/ReportServer?op=widget&widgetname=orgid&sessionID=46794'
        #----------------------------
        self.login_head = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:59.0) Gecko/20100101 Firefox/59.0',
            'Referer': 'https://sso.kedacom.com:8443/CasServer/login'
        }
        self.header_work_time = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'oa.kedacom.com',
            'Referer': 'https://oa.kedacom.com/report-manager/ReportServer?jfrom=se&reportlet=report%2F03report_sumForHour.cpt',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0',
            'X-Requested-With': 'XMLHttpRequest'
        }
    def oa_login(self):
        lt = self.getlt()
        login_data = {
            'username': self.User[0],
            'password': self.User[1],
            'lt': lt,
            'execution': 'e1s1',
            '_eventId': 'submit',
            'vcode':'',
            'submit':''
        }
        re_data =  self.post(self.login_url, login_data, self.login_head)
        return re_data

    # def Get_sessionID(self):
    #     request = urllib.request.Request('https://oa.kedacom.com/report-manager/ReportServer?jfrom=se&reportlet=report%2F03report_sumForHour.cpt')
    #     response = urllib.request.urlopen(request)
    #     return response.read().decode("utf-8")

    # def Dep_Select(self):
    #     Time_data = {
    #         '__parameters__': r"{\"LABEL0\":\"[5de5][65f6][6240][5c5e][90e8][95e8][ff1a]\",\"ORGID\":\"10000000896682\",\"LABEL1\":\"[59d3][540d][ff1a]\",\"LABEL2\":\"[8d77][59cb][65e5][671f][ff1a]\",\"BEGINDATE\":\"2018-07-10\",\"LABEL3\":\"[622a][6b62][65e5][671f][ff1a]\",\"ENDDATE\":\"2018-07-10\",\"USERID\":\"\"}"
    #     }
    #     re_data = self.post(self.select1, Time_data, self.header_work_time).content
    #     print re_data

    def Peo_Select(self):
        # data = {
        #     "limitIndex":300,
        #     "reload":"true",
        #     "stratIndex":0,
        #     "id":"1-3-4",
        #     "parentID":"1-3",
        #     "value":10000000000072,
        #     "parent_values":"[5b]\"100\",\"10000000000006\",\"10000000000072\"[5d]"
        # }
        data = {
                '__parameters__':'{\"LABEL0\": \"[5de5][65f6][6240][5c5e][90e8][95e8][ff1a]\",\"ORGID": "10000000000310",\"LABEL1": "[59d3][540d][ff1a]",\"LABEL2": "[8d77][59cb][65e5][671f][ff1a]",\"BEGINDATE\": \"2018-07-11\",\"LABEL3": \"[622a][6b62][65e5][671f][ff1a]\",\"ENDDATE\": \"2018-07-11\",\"USERID\": \"\"}'
            }
        re_data = self.post(self.select1, data, self.header_work_time)
        #print re_data.content
        s = json.loads(re_data.content.decode("GBK"))
        #print(len(s))
        #print s[0]['text']

    def Peo_Select2(self):
        # data = {
        #     "limitIndex":300,
        #     "reload":"true",
        #     "stratIndex":0,
        #     "id":"1-3-4",
        #     "parentID":"1-3",
        #     "value":10000000000072,
        #     "parent_values":"[5b]\"100\",\"10000000000006\",\"10000000000072\"[5d]"
        # }
        data = {
            '__text__':'[5b]\"100\",\"10000000000006\",\"10000000000072\",\"10000000000310\"[5d]',
            'cmd':'viewvalue',
            'limitIndex':300,
            'startIndex':0
            }
        re_data = self.post(self.select2, data, self.header_work_time)
        print re_data.content
        s = json.loads(re_data.content.decode("GBK"))
        print(len(s))
        #print s[0]['text']

    def time_work_get(self):
        '''返回数据'''
        return_list = []
        for i in self.UserList:
            print i
            print self.UserList[i]
            print self.Time[0]
            print self.Time[1]
            time_data = {
                'endDate': self.Time[0],
                'beginDate': self.Time[1],
                'userId': i,
                'pagevo': {"currentpage": 1, "pagesize": 10, "sortname": "", "sortorder": ""},
                #'status': 4
                'searchUserName': self.UserList[i]
            }
        return_time_work = self.post(self.select1,time_data, self.header_work_time)
        print return_time_work.content

    def post(self,url,data,head):
        return_data = self.se.post(url,data,head)
        return return_data

    def getlt(self):
        oa_html = self.se.get(self.login_url).text
        lt = self.get_lt_for_oa(oa_html)
        return lt

    def get_lt_for_oa(self,html):
        reg = r'<input type="hidden" name="lt" value="(.*?)" />'
        res = re.compile(reg)
        list = re.findall(res, html)
        return list[0]

    def go_main(self):
        a = oa_time_to_work(self.Time, self.User, self.UserList)
        logs.debug("开始登陆oa")
        a.oa_login()
        #a.Peo_Select()
        a.Peo_Select2()
        #a.Get_sessionID()
        #a.time_work_get()
        logs.debug("登陆oa完成")

if __name__ =="__main__":
    PI = Pruduct_ini.Pro_Ini('../Conf/conf.ini')
    User = PI.GetUserName()
    #logs.debug(User)
    UserList = PI.GetUserList()
    #EUserList = ['10000000056022']
    #logs.debug(UserList)
    time = ['2018-04-01', '2018-03-20']
    print UserList
    a = oa_time_to_work(time,User,UserList).go_main()
