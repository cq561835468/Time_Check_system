#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import logging.config
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import Pruduct_ini
import time
import re
import requests
import os
import datetime
import calendar

# logging.config.fileConfig(r'../Conf/debug.conf')
# logs = logging.getLogger('TimeWork')

class Int_Value():
    '''部门数据获取类'''
    def __init__(self,sessionID,pn=1):
        self.millis = int(round(time.time() * 1000))
        self.se = requests.session()
        self.sessionID = sessionID
        self.pn = pn
        today = datetime.date.today()
        oneday = datetime.timedelta(days=1)
        yesterday = today - oneday
        self.Time = str(yesterday)
        self.Url1 = "https://oa.kedacom.com/report-manager/ReportServer?_="+str(self.millis)+"&op=fr_form&cmd=form_getsource&sessionID="+self.sessionID+"&__widgetname__=%5B5b%5D%22USERID%22%5B5d%5D"
        self.Url2 = "https://oa.kedacom.com/report-manager/ReportServer?op=widget&widgetname=orgid&sessionID="+self.sessionID
        self.Url3 = "https://oa.kedacom.com/report-manager/ReportServer?op=fr_dialog&cmd=parameters_d&sessionID="+self.sessionID
        self.Url4 = "https://oa.kedacom.com/report-manager/ReportServer?_="+str(self.millis)+"&__boxModel__=true&op=page_content&sessionID="+self.sessionID+"&pn=1&__webpage__=true&_paperWidth=1623&_paperHeight=421&__fit__=false"
        self.header_Url1 = {
            'Accept': 'text/html, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'oa.kedacom.com',
            #'Referer': 'https://oa.kedacom.com/report-manager/ReportServer?op=fs_load&cmd=fs_signin&_=1531287633884',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0',
            'X-Requested-With': 'XMLHttpRequest'
        }

    def post(self,url,data,head):
        return_data = self.se.post(url,data,head)
        return return_data

    def Post_Por(self):
        data = {
            '__parameters__':r'{\"LABEL0\":\"[5de5][65f6][6240][5c5e][90e8][95e8][ff1a]\",\"ORGID\":\"10000000000310\",\"LABEL1\":\"[59d3][540d][ff1a]\",\"LABEL2\":\"[8d77][59cb][65e5][671f][ff1a]\",\"BEGINDATE\":\"'+self.Time+r'\",\"LABEL3\":\"[622a][6b62][65e5][671f][ff1a]\",\"ENDDATE\":\"'+self.Time+r'\",\"USERID\":\"\"}'
        }
        #print data
        #print self.Url1
        re_data = self.post(self.Url1,data,self.header_Url1)
        #print re_data
        #print re_data.content

    def Post_Por2(self):
        '''发送部门'''
        data = {
            '__text__':'[5b]\"100\",\"10000000000006\",\"10000000000072\"',
            'cmd':"viewvalue",
            'limitIndex':300,
            'startIndex':0
        }
        re_data = self.post(self.Url2, data, self.header_Url1)
        #print re_data.content

    def Post_Por3(self):
        '''点击查询按钮'''
        data = {
            '__parameters__':'{\"LABEL0\":\"[5de5][65f6][6240][5c5e][90e8][95e8][ff1a]\",\"ORGID\":\"10000000000072\",\"LABEL1\":\"[59d3][540d][ff1a]\",\"LABEL2\":\"[8d77][59cb][65e5][671f][ff1a]\",\"BEGINDATE\":\"'+self.Time+'\",\"LABEL3\":\"[622a][6b62][65e5][671f][ff1a]\",\"ENDDATE\":\"'+self.Time+'\",\"USERID\":\"\"}'
        }
        re_data = self.post(self.Url3, data, self.header_Url1)
        print re_data.content
#
    def Get_Value(self):
        re_data = self.se.get(self.Url4)
        #print self.Url4
        return re_data.content

    def get_light(self,html):
        '''匹配原图地址的正则表达式'''
        reg = r'reportTotalPage=(\d+)'
        imgre = re.compile(reg)
        imglist = re.findall(imgre, html)
        return imglist

    def run(self):
        '''主函数'''
        print "day time begin!"
        self.Post_Por()
        self.Post_Por2()
        self.Post_Por3()
        html = self.Get_Value()
        #print "html is %s" % html
        html_doc = html.decode("gbk", "ignore")
        #print html_doc
        if int(self.get_light(html_doc.encode('utf-8'))[0]) <= self.pn:
            f = open(os.getcwd() + '\\' + '\data_all\data_all_' + str(self.pn) + '.html', 'w')
            f.write(html_doc.encode('utf-8'))
            f.close()
            print "finish"
        else:
            print self.pn
            f = open(os.getcwd() + '\\'+'\data_all\data_all_'+str(self.pn)+'.html','w')
            f.write(html_doc.encode('utf-8'))
            f.close()
            self.pn += 1
            Int_Value(self.sessionID,pn=self.pn).run()
        # f = open(os.getcwd()+'\\'+'data.html','w')
        # f.write(html_doc.encode('utf-8'))
        # f.close()

class Int_Value_Project():
    '''项目数据获取类'''
    def __init__(self,sessionID):
        self.millis = int(round(time.time() * 1000))
        self.se = requests.session()
        self.sessionID = sessionID
        today = datetime.date.today()
        oneday = datetime.timedelta(days=1)
        yesterday = today - oneday
        self.Time = str(yesterday)
        self.Url1 = "https://oa.kedacom.com/report-manager/ReportServer?op=fr_dialog&cmd=parameters_d&sessionID="+self.sessionID
        self.Url2 = "https://oa.kedacom.com/report-manager/ReportServer?_="+str(self.millis)+"&__boxModel__=true&op=fr_write&cmd=read_w_content&sessionID="+self.sessionID+"&reportIndex=0&browserWidth=1653&iid=0.11175721501266733&__cutpage__=&pn=0&__webpage__=true&_paperWidth=1653&_paperHeight=377&__fit__=false"
        self.header_Url1 = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'oa.kedacom.com',
            #'Referer': 'https://oa.kedacom.com/report-manager/ReportServer?op=fs_load&cmd=fs_signin&_=1531287633884',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0',
            'X-Requested-With': 'XMLHttpRequest'
        }

    def post(self,url,data,head):
        return_data = self.se.post(url,data,head)
        return return_data

    def Post_Para(self):
        data = {
            #'__parameters__':r'{"ORGPATHPRO":"1.100.10000000000006.10000000000072.","LABELORGID_C_C_C":"[9879][76ee][6240][5c5e][90e8][95e8]:","HOURSTATE":"4","LABEL0_C":"[5de5][65f6][72b6][6001]:","LABELORGID_C_C":"[5458][5de5][59d3][540d]:","FULLNAME":"","PROJECTNAME":"","LABELPROJECTNAME":"[9879][76ee][540d][79f0]:","ORGID":"","LABELORGID":"[5de5][65f6][6240][5c5e][90e8][95e8]:","PROJECTCODE":"","LABELPROJECTCODE":"[9879][76ee][7f16][7801]:","ENDDATE":'+ self.Time + r',"LABELENDDATE":"*[7ed3][675f][65e5][671f]:","BEGINDATE":'+ self.Time + r',"LABELBEGINDATE":"*[5f00][59cb][65e5][671f]:"}'
            #'__parameters__':r'{"ORGPATHPRO":"","LABELORGID_C_C_C":"[9879][76ee][6240][5c5e][90e8][95e8]:","HOURSTATE":"4","LABEL0_C":"[5de5][65f6][72b6][6001]:","LABELORGID_C_C":"[5458][5de5][59d3][540d]:","FULLNAME":"","PROJECTNAME":"","LABELPROJECTNAME":"[9879][76ee][540d][79f0]:","ORGID":"1.100.10000000000006.10000000000072.","LABELORGID":"[5de5][65f6][6240][5c5e][90e8][95e8]:","PROJECTCODE":"","LABELPROJECTCODE":"[9879][76ee][7f16][7801]:","ENDDATE":2018-08-29,"LABELENDDATE":"*[7ed3][675f][65e5][671f]:","BEGINDATE":2018-01-01,"LABELBEGINDATE":"*[5f00][59cb][65e5][671f]:"}'
            #'__parameters__':r'{"ORGPATHPRO":"1.100.10000000000006.10000000000072.","LABELORGID_C_C_C":"[9879][76ee][6240][5c5e][90e8][95e8]:","HOURSTATE":"4","LABEL0_C":"[5de5][65f6][72b6][6001]:","LABELORGID_C_C":"[5458][5de5][59d3][540d]:","FULLNAME":"","PROJECTNAME":"","LABELPROJECTNAME":"[9879][76ee][540d][79f0]:","ORGID":"","LABELORGID":"[5de5][65f6][6240][5c5e][90e8][95e8]:","PROJECTCODE":"","LABELPROJECTCODE":"[9879][76ee][7f16][7801]:","ENDDATE":"2018-08-29","LABELENDDATE":"*[7ed3][675f][65e5][671f]:","BEGINDATE":"2018-01-01","LABELBEGINDATE":"*[5f00][59cb][65e5][671f]:"}'
            '__parameters__':r'{"ORGPATHPRO":"1.100.10000000000006.10000000000072.","LABELORGID_C_C_C":"[9879][76ee][6240][5c5e][90e8][95e8]:","HOURSTATE":"4","LABEL0_C":"[5de5][65f6][72b6][6001]:","LABELORGID_C_C":"[5458][5de5][59d3][540d]:","FULLNAME":"","PROJECTNAME":"","LABELPROJECTNAME":"[9879][76ee][540d][79f0]:","ORGID":"","LABELORGID":"[5de5][65f6][6240][5c5e][90e8][95e8]:","PROJECTCODE":"","LABELPROJECTCODE":"[9879][76ee][7f16][7801]:","ENDDATE":' + self.Time + r',"LABELENDDATE":"*[7ed3][675f][65e5][671f]:","BEGINDATE":'+ self.Time + r',"LABELBEGINDATE":"*[5f00][59cb][65e5][671f]:"}'
        }
        #print data
        #print "self.Url1 is " + self.Url1
        re_data = self.post(self.Url1,data,self.header_Url1)
        #print "re_data.content is " + re_data.content

    def Get_Value(self,url):
        re_data = self.se.get(url)
        return re_data.content

    def get_light(self,html):
        '''匹配原图地址的正则表达式'''
        reg = r'heavytd=\"light\">.*<\/div><\/td><td class='
        imgre = re.compile(reg)
        imglist = re.findall(imgre, html)
        return imglist

    def run(self):
        '''主函数'''
        self.Post_Para()
        html = self.Get_Value(self.Url2)
        html_doc = html.decode("gbk", "ignore")
        #print html_doc.encode('utf-8')
        f = open(os.getcwd()+'\\'+'data_pro.html','w')
        f.write(html_doc.encode('utf-8'))
        f.close()

class Int_Value_Week():
    '''部门数据获取类，每周1-4工时情况'''
    def __init__(self,sessionID,day,pn=1):
        self.millis = int(round(time.time() * 1000))
        self.se = requests.session()
        self.sessionID = sessionID
        self.pn = pn
        self.day = day
        today = datetime.date.today()
        oneday = datetime.timedelta(days=self.day)
        oneday_2 = datetime.timedelta(days=1)
        bef_monday = today - oneday
        yestday = today - oneday_2
        self.yestday = str(yestday)
        print self.yestday
        self.bef_monday = str(bef_monday)
        print self.bef_monday
        self.Url1 = "https://oa.kedacom.com/report-manager/ReportServer?_="+str(self.millis)+"&op=fr_form&cmd=form_getsource&sessionID="+self.sessionID+"&__widgetname__=%5B5b%5D%22USERID%22%5B5d%5D"
        self.Url2 = "https://oa.kedacom.com/report-manager/ReportServer?op=widget&widgetname=orgid&sessionID="+self.sessionID
        self.Url3 = "https://oa.kedacom.com/report-manager/ReportServer?op=fr_dialog&cmd=parameters_d&sessionID="+self.sessionID
        self.Url4 = "https://oa.kedacom.com/report-manager/ReportServer?_="+str(self.millis)+"&__boxModel__=true&op=page_content&sessionID="+self.sessionID+"&pn="+str(self.pn)+"&__webpage__=true&_paperWidth=1623&_paperHeight=9999&__fit__=false"
        self.header_Url1 = {
            'Accept': 'text/html, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'oa.kedacom.com',
            #'Referer': 'https://oa.kedacom.com/report-manager/ReportServer?op=fs_load&cmd=fs_signin&_=1531287633884',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0',
            'X-Requested-With': 'XMLHttpRequest'
        }

    def get_light(self,html):
        '''匹配原图地址的正则表达式'''
        reg = r'heavytd=\"light\">.*<\/div><\/td><td class='
        imgre = re.compile(reg)
        imglist = re.findall(imgre, html)
        return imglist

    def post(self,url,data,head):
        return_data = self.se.post(url,data,head)
        return return_data

    def Post_Por(self):
        data = {
            '__parameters__':r'{\"LABEL0\":\"[5de5][65f6][6240][5c5e][90e8][95e8][ff1a]\",\"ORGID\":\"10000000000310\",\"LABEL1\":\"[59d3][540d][ff1a]\",\"LABEL2\":\"[8d77][59cb][65e5][671f][ff1a]\",\"BEGINDATE\":\"'+self.bef_monday+r'\",\"LABEL3\":\"[622a][6b62][65e5][671f][ff1a]\",\"ENDDATE\":\"'+self.yestday+r'\",\"USERID\":\"\"}'
        }
        print data
        #print self.Url1
        re_data = self.post(self.Url1,data,self.header_Url1)
        #print re_data
        #print re_data.content

    def Post_Por2(self):
        '''发送部门'''
        data = {
            '__text__':'[5b]\"100\",\"10000000000006\",\"10000000000072\"',
            'cmd':"viewvalue",
            'limitIndex':300,
            'startIndex':0
        }
        re_data = self.post(self.Url2, data, self.header_Url1)
        #print re_data.content

    def Post_Por3(self):
        '''点击查询按钮'''
        data = {
            '__parameters__':'{\"LABEL0\":\"[5de5][65f6][6240][5c5e][90e8][95e8][ff1a]\",\"ORGID\":\"10000000000072\",\"LABEL1\":\"[59d3][540d][ff1a]\",\"LABEL2\":\"[8d77][59cb][65e5][671f][ff1a]\",\"BEGINDATE\":\"'+self.bef_monday+'\",\"LABEL3\":\"[622a][6b62][65e5][671f][ff1a]\",\"ENDDATE\":\"'+self.yestday+'\",\"USERID\":\"\"}'
        }
        re_data = self.post(self.Url3, data, self.header_Url1)
        #print re_data.content

    def Get_Value(self):
        re_data = self.se.get(self.Url4)
        return re_data.content

    def get_light(self,html):
        '''匹配原图地址的正则表达式'''
        reg = r'reportTotalPage=(\d+)'
        imgre = re.compile(reg)
        imglist = re.findall(imgre, html)
        return imglist

    def run(self):
        '''主函数'''
        self.Post_Por()
        self.Post_Por2()
        self.Post_Por3()
        html = self.Get_Value()
        html_doc = html.decode("gbk", "ignore")
        #print html_doc.encode('utf-8')
        print self.get_light(html_doc.encode('utf-8'))
        if int(self.get_light(html_doc.encode('utf-8'))[0]) < self.pn:
            f = open(os.getcwd()+'\\'+'data.html','w')
            f.write(html_doc.encode('utf-8'))
            f.close()
            print "finish"
        else:
            print self.pn
            f = open(os.getcwd()+'\\'+'\data_all\data_all_'+str(self.pn)+'.html','w')
            f.write(html_doc.encode('utf-8'))
            f.close()
            self.pn += 1
            Int_Value_Week(self.sessionID,day=self.day,pn=self.pn).run()

class Int_Value_Month():
    '''部门数据获取类，每月工时情况'''
    def __init__(self,sessionID,pn=1):
        self.millis = int(round(time.time() * 1000))
        self.se = requests.session()
        self.sessionID = sessionID
        self.pn = pn
        if self.JuDataMoLast() == False:
            raise RuntimeError('Not Last Day!')
        self.bef_monday = self.JuDataMoLast()[0]
        self.yestday = self.JuDataMoLast()[1]
        self.Url1 = "https://oa.kedacom.com/report-manager/ReportServer?_="+str(self.millis)+"&op=fr_form&cmd=form_getsource&sessionID="+self.sessionID+"&__widgetname__=%5B5b%5D%22USERID%22%5B5d%5D"
        self.Url2 = "https://oa.kedacom.com/report-manager/ReportServer?op=widget&widgetname=orgid&sessionID="+self.sessionID
        self.Url3 = "https://oa.kedacom.com/report-manager/ReportServer?op=fr_dialog&cmd=parameters_d&sessionID="+self.sessionID
        self.Url4 = "https://oa.kedacom.com/report-manager/ReportServer?_="+str(self.millis)+"&__boxModel__=true&op=page_content&sessionID="+self.sessionID+"&pn="+str(self.pn)+"&__webpage__=true&_paperWidth=1623&_paperHeight=9999&__fit__=false"
        self.header_Url1 = {
            'Accept': 'text/html, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'oa.kedacom.com',
            #'Referer': 'https://oa.kedacom.com/report-manager/ReportServer?op=fs_load&cmd=fs_signin&_=1531287633884',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0',
            'X-Requested-With': 'XMLHttpRequest'
        }

    def JuDataMoLast(self):
        '''判断是否为当月最后一天'''
        today = str(datetime.date.today())
        day_now = time.localtime()
        day_begin = '%d-%02d-01' % (day_now.tm_year, day_now.tm_mon)
        wday, monthRange = calendar.monthrange(day_now.tm_year, day_now.tm_mon)
        day_end = '%d-%02d-%02d' % (day_now.tm_year, day_now.tm_mon, monthRange)
        print "day_now is %s" % day_now
        print "day_end is %s" % day_end
        print "today is %s" % today
        if today == day_end:
            return [day_begin,day_end]
        return False

    def get_light(self,html):
        '''匹配原图地址的正则表达式'''
        reg = r'heavytd=\"light\">.*<\/div><\/td><td class='
        imgre = re.compile(reg)
        imglist = re.findall(imgre, html)
        return imglist

    def post(self,url,data,head):
        return_data = self.se.post(url,data,head)
        return return_data

    def Post_Por(self):
        data = {
            '__parameters__':r'{\"LABEL0\":\"[5de5][65f6][6240][5c5e][90e8][95e8][ff1a]\",\"ORGID\":\"10000000000310\",\"LABEL1\":\"[59d3][540d][ff1a]\",\"LABEL2\":\"[8d77][59cb][65e5][671f][ff1a]\",\"BEGINDATE\":\"'+self.bef_monday+r'\",\"LABEL3\":\"[622a][6b62][65e5][671f][ff1a]\",\"ENDDATE\":\"'+self.yestday+r'\",\"USERID\":\"\"}'
        }
        print "*" *10+"Post_Por"+"*" *10
        print data
        #print self.Url1
        re_data = self.post(self.Url1,data,self.header_Url1)
        #print re_data
        #print re_data.content

    def Post_Por2(self):
        '''发送部门'''
        data = {
            '__text__':'[5b]\"100\",\"10000000000006\",\"10000000000072\"',
            'cmd':"viewvalue",
            'limitIndex':300,
            'startIndex':0
        }
        re_data = self.post(self.Url2, data, self.header_Url1)
        #print re_data.content

    def Post_Por3(self):
        '''点击查询按钮'''
        data = {
            '__parameters__':'{\"LABEL0\":\"[5de5][65f6][6240][5c5e][90e8][95e8][ff1a]\",\"ORGID\":\"10000000000072\",\"LABEL1\":\"[59d3][540d][ff1a]\",\"LABEL2\":\"[8d77][59cb][65e5][671f][ff1a]\",\"BEGINDATE\":\"'+self.bef_monday+'\",\"LABEL3\":\"[622a][6b62][65e5][671f][ff1a]\",\"ENDDATE\":\"'+self.yestday+'\",\"USERID\":\"\"}'
        }
        re_data = self.post(self.Url3, data, self.header_Url1)
        print "*" *10+"Post_Por3"+"*" *10
        #print re_data.content

    def Get_Value(self):
        re_data = self.se.get(self.Url4)
        return re_data.content

    def get_light(self,html):
        '''匹配原图地址的正则表达式'''
        reg = r'reportTotalPage=(\d+)'
        imgre = re.compile(reg)
        imglist = re.findall(imgre, html)
        return imglist

    def run(self):
        '''主函数'''
        self.Post_Por()
        self.Post_Por2()
        self.Post_Por3()
        html = self.Get_Value()
        html_doc = html.decode("gbk", "ignore")
        #print html_doc.encode('utf-8')
        print self.get_light(html_doc.encode('utf-8'))
        if int(self.get_light(html_doc.encode('utf-8'))[0]) < self.pn:
            f = open(os.getcwd()+'\\'+'data.html','w')
            f.write(html_doc.encode('utf-8'))
            f.close()
            print "finish"
        else:
            print self.pn
            f = open(os.getcwd()+'\\'+'\data_all\data_all_'+str(self.pn)+'.html','w')
            f.write(html_doc.encode('utf-8'))
            f.close()
            self.pn += 1
            Int_Value_Month(self.sessionID,pn=self.pn).run()

class Selenium_Oa():
    def __init__(self,User):
        self.User = User
        #profile = webdriver.FirefoxProfile('C:\Users\Administrator\Desktop\cq')  # 配置文件路径变量
        options = webdriver.FirefoxOptions()
        #options.set_headless()
        self.driver = webdriver.Firefox(firefox_options=options)
        # self.driver = webdriver.Firefox(profile)
        # self.driver.maximize_window()

    def Go_To_Page(self):
        '''进入工时查询页面'''
        self.driver.get("https://sso.kedacom.com:8443/CasServer/login")
        self.driver.find_element_by_id("ui_username").send_keys(self.User[0])
        self.driver.find_element_by_id("ui_password").send_keys(self.User[1])
        self.driver.find_element_by_id("ui_username").click() 
        self.driver.find_element_by_id("submit_login").click()
        self.driver.get("https://oa.kedacom.com/report/platform/console/main.do")
        arrw_inner = self.driver.find_elements_by_class_name("l-accordion-header-inner")
        arrw_inner[1].click()
        arrw_span = self.driver.find_elements_by_tag_name('span')
        arrw_span[4].click()

    def Error_Session(self):
        self.driver.get("https://oa.kedacom.com/report/platform/console/main.do")
        arrw_inner = self.driver.find_elements_by_class_name("l-accordion-header-inner")
        arrw_inner[1].click()
        arrw_span = self.driver.find_elements_by_tag_name('span')
        arrw_span[4].click()

    def Check_in(self,session):
        '检查session值'
        if session == []:
            self.Error_Session()
            time.sleep(3)
            self.driver.switch_to.frame("kdUIFrameWindow")
            html = self.driver.page_source #获取页面源码
            self.sessionID = self.get_session(html) #获取sessionID
            print self.sessionID 
            self.Check_in(self.sessionID)
        else:
            pass
            #self.session = sessionID
            #return session


    def get_session(self,html):
        '''匹配SessionID正则表达式'''
        #reg = r'https://i.pximg.net/img-original/img/(.*?)'
        #print html
        reg = r'FR.SessionMgr.register\(\'(.*)\', contentPane\);'
        imgre = re.compile(reg)
        imglist = re.findall(imgre, html)
        return imglist

    def run(self):
        '''主函数'''
        self.Go_To_Page()  #进入工时页面
        time.sleep(3)
        self.driver.switch_to.frame("kdUIFrameWindow")
        html = self.driver.page_source #获取页面源码
        self.sessionID = self.get_session(html) #获取sessionID
        self.Check_in(self.sessionID)
        print self.sessionID
        Int_Value(self.sessionID[0].encode("utf-8")).run()
        self.driver.quit()
        # else:
            # print "error sessionID"
        #logs.debug(u"数据导出完成")
        #print u"数据导出完成"

class Selenium_Oa_Project():
    def __init__(self,User):
        self.User = User
        #profile = webdriver.FirefoxProfile('C:\Users\Administrator\Desktop\cq')  # 配置文件路径变量
        options = webdriver.FirefoxOptions()
        options.set_headless()
        self.driver = webdriver.Firefox(firefox_options=options)
        # self.driver = webdriver.Firefox(profile)
        # self.driver.maximize_window()

    def Go_To_Page(self):
        '''进入工时查询页面'''
        self.driver.get("https://sso.kedacom.com:8443/CasServer/login")
        self.driver.find_element_by_id("ui_username").send_keys(self.User[0])
        self.driver.find_element_by_id("ui_password").send_keys(self.User[1])
        self.driver.find_element_by_class_name("btn").click()
        self.driver.get("https://oa.kedacom.com/report/platform/console/main.do")
        arrw_inner = self.driver.find_elements_by_class_name("l-accordion-header-inner")
        arrw_inner[1].click()
        arrw_span = self.driver.find_elements_by_tag_name('span')
        arrw_span[6].click()

    def Error_Session(self):
        self.driver.get("https://oa.kedacom.com/report/platform/console/main.do")
        arrw_inner = self.driver.find_elements_by_class_name("l-accordion-header-inner")
        arrw_inner[1].click()
        arrw_span = self.driver.find_elements_by_tag_name('span')
        arrw_span[6].click()
        
    def get_session(self,html):
        '''匹配SessionID正则表达式'''
        #reg = r'https://i.pximg.net/img-original/img/(.*?)'
        #print html
        reg = r'FR.SessionMgr.register\(\'(.*)\', contentPane\);'
        imgre = re.compile(reg)
        imglist = re.findall(imgre, html)
        return imglist

    def run(self):
        '''主函数'''
        self.Go_To_Page()  #进入工时页面
        time.sleep(3)
        self.driver.switch_to.frame("kdUIFrameWindow")
        html = self.driver.page_source #获取页面源码
        sessionID = self.get_session(html) #获取sessionID
        print sessionID
        if sessionID == []:
            self.Error_Session()
        else:
            Int_Value_Project(sessionID[0].encode("utf-8")).run()
            self.driver.quit()
        #logs.debug(u"数据导出完成")
        #print u"数据导出完成"

class Selenium_Oa_week():
    def __init__(self,User,day):
        self.User = User
        self.day = day
        #profile = webdriver.FirefoxProfile('C:\Users\Administrator\Desktop\cq')  # 配置文件路径变量
        options = webdriver.FirefoxOptions()
        #options.set_headless()
        self.driver = webdriver.Firefox(firefox_options=options)
        # self.driver = webdriver.Firefox(profile)
        # self.driver.maximize_window()

    def Go_To_Page(self):
        '''进入工时查询页面'''
        self.driver.get("https://sso.kedacom.com:8443/CasServer/login")
        self.driver.find_element_by_id("ui_username").send_keys(self.User[0])
        self.driver.find_element_by_id("ui_password").send_keys(self.User[1])
        self.driver.find_element_by_class_name("btn").click()
        self.driver.get("https://oa.kedacom.com/report/platform/console/main.do")
        arrw_inner = self.driver.find_elements_by_class_name("l-accordion-header-inner")
        arrw_inner[1].click()
        arrw_span = self.driver.find_elements_by_tag_name('span')
        arrw_span[4].click()

    def get_session(self,html):
        '''匹配SessionID正则表达式'''
        #reg = r'https://i.pximg.net/img-original/img/(.*?)'
        #print html
        reg = r'FR.SessionMgr.register\(\'(.*)\', contentPane\);'
        imgre = re.compile(reg)
        imglist = re.findall(imgre, html)
        return imglist

    def run(self):
        '''主函数'''
        self.Go_To_Page()  #进入工时页面
        time.sleep(3)
        self.driver.switch_to.frame("kdUIFrameWindow")
        html = self.driver.page_source #获取页面源码
        sessionID = self.get_session(html) #获取sessionID
        Int_Value_Week(sessionID[0].encode("utf-8"),day=self.day).run()
        self.driver.quit()
        #logs.debug(u"数据导出完成")
        #print u"数据导出完成"

class Selenium_Oa_Month():
    def __init__(self,User):
        self.User = User
        #profile = webdriver.FirefoxProfile('C:\Users\Administrator\Desktop\cq')  # 配置文件路径变量
        options = webdriver.FirefoxOptions()
        options.set_headless()
        self.driver = webdriver.Firefox(firefox_options=options)
        # self.driver = webdriver.Firefox(profile)
        # self.driver.maximize_window()

    def Go_To_Page(self):
        '''进入工时查询页面'''
        self.driver.get("https://sso.kedacom.com:8443/CasServer/login")
        self.driver.find_element_by_id("ui_username").send_keys(self.User[0])
        self.driver.find_element_by_id("ui_password").send_keys(self.User[1])
        self.driver.find_element_by_class_name("btn").click()
        self.driver.get("https://oa.kedacom.com/report/platform/console/main.do")
        arrw_inner = self.driver.find_elements_by_class_name("l-accordion-header-inner")
        arrw_inner[1].click()
        arrw_span = self.driver.find_elements_by_tag_name('span')
        arrw_span[4].click()

    def Error_Session(self):
        self.driver.get("https://oa.kedacom.com/report/platform/console/main.do")
        arrw_inner = self.driver.find_elements_by_class_name("l-accordion-header-inner")
        arrw_inner[1].click()
        arrw_span = self.driver.find_elements_by_tag_name('span')
        arrw_span[4].click()
        

    def get_session(self,html):
        '''匹配SessionID正则表达式'''
        #reg = r'https://i.pximg.net/img-original/img/(.*?)'
        #print html
        reg = r'FR.SessionMgr.register\(\'(.*)\', contentPane\);'
        imgre = re.compile(reg)
        imglist = re.findall(imgre, html)
        return imglist

    def run(self):
        '''主函数'''
        self.Go_To_Page()  #进入工时页面
        time.sleep(3)
        self.driver.switch_to.frame("kdUIFrameWindow")
        html = self.driver.page_source #获取页面源码
        sessionID = self.get_session(html) #获取sessionID
        if sessionID == []:
            self.Error_Session()
        else:
            Int_Value_Month(sessionID[0].encode("utf-8")).run()
            self.driver.quit()
        #logs.debug(u"数据导出完成")
        #print u"数据导出完成"


if __name__ == "__main__":
    PI = Pruduct_ini.Pro_Ini('../Conf/conf.ini')
    User = PI.GetUserName() #登录用户名
    De = Selenium_Oa(User).run()
