#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup
import os
import Pruduct_ini
import datetime
import re
import calendar
import time

class Data_V():
    '''每日工时处理'''
    def __init__(self):
        if os.path.exists(os.getcwd() + r'\\'+r'Report\report.html'):
            os.remove(os.path.abspath(os.getcwd() + r'\\'+ r'Report\report.html'))
        self.soup_new = BeautifulSoup(open(os.getcwd()+ r'\\' + r'Conf\report.html'), 'lxml')
        self.list_file = self.GetDir(os.getcwd() + r'\\' + 'data_all')  # 获取所有文件

    def GetDir(self, path):
        '''获取该设备所有模块/获取该模块下所有请求'''
        list_dir = []
        dirs = os.listdir(path)
        for i in dirs:
            list_dir.append(i)
        return list_dir

    def is_Chinese(self,word):
        for ch in word.decode('utf-8'):
            if u'\u4e00' <= ch <= u'\u9fff':
                return True
        return False

    def GetPeople(self,td_all,Userlist):
        '''获取用户名'''
        arrw_name = []
        for num, i in enumerate(td_all):
            x = i.get_text().encode("utf-8")
            #print num,x
            if self.is_Chinese(x):
                arrw_name.append(num)
        arrw_name.append(len(td_all))
        return arrw_name

    def Pool_Soap(self,arrw_name,td_all):
        '''汇总所有html数据，放入字典中'''
        for xx in range(0, len(arrw_name) - 1):
            #print td_all[arrw_name[xx]].get_text().encode("utf-8")
            tmp_arr, num = [], 0
            # print arrw_name[xx + 1]
            for xxx in range(arrw_name[xx] + 1, arrw_name[xx + 1]):
                if num == 5:  # 5个清空
                    # print td_all[xxx].get_text().encode("utf-8")
                    self.list_all[td_all[arrw_name[xx]].get_text().encode("utf-8")].append(tmp_arr)
                    tmp_arr, num = [], 0
                tmp_arr.append(td_all[xxx].get_text().encode("utf-8"))
                num += 1
                if xxx == arrw_name[xx + 1] - 1:  # 最后一次
                    #self.list_all[td_all[arrw_name[xx]].get_text().encode("utf-8")].append(tmp_arr)
                    self.list_all[td_all[arrw_name[xx]].get_text().encode("utf-8")] = tmp_arr[:]
                #print tmp_arr

    def Sum_Pool(self):
        '''汇总工时数据'''
        for key in self.list_all:
            tmp_value = 0
            for x in self.list_all[key]:
                for xx in range(3,5):
                    if xx == 2:
                        continue
                    tmp_value += float(x[xx])
            if tmp_value >= 40:
                self.Sum_list_all_t[key] = tmp_value
            else:
                self.Sum_list_all_f[key] = tmp_value


    def Miss_Time(self,list_s):
        '''统计漏填工时人员'''
        list_tmp = {}
        for key in list_s:
            num = float(list_s[key][1])+float(list_s[key][3])+float(list_s[key][4])
            if num < 7.5 and num !=0:
                list_tmp[key] = list_s[key]
        return list_tmp

    def Not_Time(self,list_s):
        '''统计未填工时人员'''
        list_tmp = {}
        for key in list_s:
            num = float(list_s[key][1])+float(list_s[key][2])+float(list_s[key][3])+float(list_s[key][4])
            if num == 0:
                list_tmp[key] = list_s[key]
        return list_tmp

    def Not_Post_Time(self,list_s):
        '''统计未提交工时人员'''
        list_tmp = {}
        for key in list_s:
            num = float(list_s[key][1])
            if num > 0:
                list_tmp[key] = list_s[key]
        return list_tmp

    def OK_Time(self,list_s):
        '''统计正确工时人员'''
        list_tmp = {}
        for key in list_s:
            num = float(list_s[key][1])+float(list_s[key][3])+float(list_s[key][4])
            if num > 7.5:
                list_tmp[key] = list_s[key]
        return list_tmp

    def Group_In_Dict(self,data,group):
        '''写入组关联'''
        listre = {}
        for x in data:
            for xx in group:
                if x in group[xx].keys():
                    if listre.has_key(xx): #如果字典listre中存在该部门key
                        listre[xx][x] = data[x] #部门中再加字典代表个人工时{部门:{人员:时间}}
                    else:
                        listre[xx] = {}
                        listre[xx][x] = data[x]
        return listre



    def Insert_Table(self,tables,values,key="empty"):
        '''插入表'''
        if key != "Info_Dep":
            new_tr1 = self.soup_new.new_tag('tr')  # 添加tr标签-表头
            tables.append(new_tr1)
            listr = ["姓名/内容","日期","未提交工时数","被驳回工时数","待审批工时数","审批通过工时数"]
            for key,value in enumerate(listr):
                heads = self.soup_new.new_tag('th')
                new_tr1.insert(key,heads)
                heads.string = value
        #############################表头###########################
        for branch in values: #部门
            new_tr2 = self.soup_new.new_tag('tr')  # 添加tr标签
            tables.append(new_tr2)
            branch_s = self.soup_new.new_tag('th')
            new_tr2.insert(0,branch_s)
            branch_s.string = branch
            branch_s.attrs['colspan']="6"
            # branch_s.attrs['style'] = "text-align: center;"
            for x in values[branch]: #人员
                new_tr3 = self.soup_new.new_tag('tr')  # 添加tr标签
                tables.append(new_tr3)
                print x,values[branch][x]
                list = [x]
                for x in values[branch][x]:
                    list.append(x)
                for key,value in enumerate(list):
                    branch_s = self.soup_new.new_tag('td')
                    new_tr3.insert(key, branch_s)
                    branch_s.string = value

    def Insert_Table_Resule(self, tables, values):
        for key in values:
            new_tr1 = self.soup_new.new_tag('tr')  # 添加tr标签
            tables.append(new_tr1)
            #------------添加行数据-------------
            td_data = self.soup_new.new_tag('td')
            new_tr1.insert(0, td_data)
            td_data.string = str(key)
            for num,keyss in enumerate(values[key]):
                td_data = self.soup_new.new_tag('td')
                new_tr1.insert(num+1, td_data)
                td_data.string = str(keyss)

    def new_report(self,OK_Arrw,Not_Arrw,Not_Post_Time_Arrw,Miss_Time,Info_Dep):
        '''模板生成新html'''
        table1 = self.soup_new('table')  #获得表
        #print Miss_Time
        self.Insert_Table(table1[0], Miss_Time)  # 插入漏填工时表
        self.Insert_Table(table1[1], Not_Arrw)  # 插入未填工时表
        self.Insert_Table(table1[2], Not_Post_Time_Arrw)  # 插入未提交工时表
        self.Insert_Table(table1[3], OK_Arrw)  #插入正确工时表
        self.Insert_Table(table1[4], Info_Dep,"Info_Dep") #插入明细表
        sa = open(os.getcwd() + r'\\'+r'Report\report.html','w')
        sa.write(str(self.soup_new))
        sa.close()

    def run(self,Userlist,GroupList,Group_Info):
        self.list_all = {} #所有数据
        self.Sun_Data = {} #所有统计完成数据
        for x in Userlist:
            self.list_all[x] = []
        #---------------------------
        for filename in self.list_file:
            self.soup = BeautifulSoup(open(os.getcwd() + r'\\' + 'data_all'+ r'\\'+filename), 'lxml')
            td_all = self.soup.findAll("div")[14:]
            for x in td_all:
                if x.get_text().encode("utf-8") in GroupList:
                    td_all.remove(x)
            arrw_name = self.GetPeople(td_all,Userlist) #获取每页所有查询出来的人员下标
            #print "arrw_name is %s" % arrw_name
            for x in arrw_name[:-1]:
                '''不存在则创建key'''
                if td_all[x].get_text().encode("utf-8") in self.list_all.keys():
                    pass
                else:
                    self.list_all[td_all[x].get_text().encode("utf-8")] = []
            self.Pool_Soap(arrw_name,td_all) #汇总所有html数据，放入字典中
        # print arrw_name
        # print td_all
        # print self.list_all
        # for x in self.list_all:
        #     print x,self.list_all[x]
        OK_Arrw = self.Group_In_Dict(self.OK_Time(self.list_all),Group_Info)
        Not_Arrw = self.Group_In_Dict(self.Not_Time(self.list_all),Group_Info)
        Not_Post_Time_Arrw = self.Group_In_Dict(self.Not_Post_Time(self.list_all),Group_Info)
        Miss_Time = self.Group_In_Dict(self.Miss_Time(self.list_all),Group_Info)
        Info_Dep = self.Group_In_Dict(self.list_all, Group_Info)
        # print self.Not_Time(self.list_all)
        for x in self.Not_Post_Time(self.list_all):
            print x
        self.new_report(OK_Arrw,Not_Arrw,Not_Post_Time_Arrw,Miss_Time,Info_Dep)
        # print self.Miss_Time(self.list_all)
        #self.Group_In_Dict(self.Miss_Time(self.list_all), Group_Info)
        # for x in self.Group_In_Dict(self.Miss_Time(self.list_all),Group_Info):
        #     print x,self.Group_In_Dict(self.Miss_Time(self.list_all),Group_Info)[x]
        # for x in self.Group_In_Dict(self.Miss_Time(self.list_all),Group_Info):
        #     print x,self.Group_In_Dict(self.Miss_Time(self.list_all),Group_Info)[x]
        # for x in self.Miss_Time(self.list_all):
        #     print x,self.Miss_Time(self.list_all)[x]
        #     for xx in self.Miss_Time(self.list_all)[x]:
        #         print xx,self.Miss_Time(self.list_all)[x][xx]
        # for x in OK_Arrw:
        #     print x,OK_Arrw[x]
        # for x in OK_Arrw:
        #     print "%s:%s" % (x,OK_Arrw[x])
        # for x in [OK_Arrw,Not_Arrw,Not_Post_Time_Arrw,Miss_Time]:
        #     self.Group_In_Dict(x,Group_Info)
        # for x in self.list_all:
        #     #print self.list_all[x]
        #     self.Group_In_Dict(x, Group_Info)

        #print self.Sun_Data
        #     #self.Sum_Pool_No_Sumbit(arrw_name,td_all) #汇总所有html数据，放入字典中(未提交的数据)
        #     self.Sum_Pool()
        # self.new_report(self.Sun_Data,Group_Info)
        # list_all = {}
        # td_all = self.soup.findAll("div")
        # for num, i in enumerate(td_all):
        #     x = i.get_text().encode("utf-8")
        #     #print num, i.get_text()
        #     #print x
        #     if x in Userlist:
        #         list_tmp =[]
        #         for xx in range(1,6):
        #             list_tmp.append(td_all[num+xx].get_text().encode("utf-8"))
        #             #print td_all[num+xx].get_text().encode("utf-8")
        #         list_all[x] = list_tmp
        # Miss_Time = self.Miss_Time(list_all) #漏填工时
        # Not_Time = self.Not_Time(list_all)  # 未填工时
        # Not_Post_Time = self.Not_Post_Time(list_all) #未提交
        # OK_Time = self.OK_Time(list_all) #正确的工时
        # print "------漏填工时-------"
        # print Miss_Time
        # print "------未填工时-------"
        # print Not_Time
        # print "------未提交工时-------"
        # print Not_Post_Time
        # print "------正确的工时-------"
        # print OK_Time
        # self.new_report(Miss_Time,Not_Time,Not_Post_Time,OK_Time,list_all)

        # for i in OK_Time:
        #     print i,OK_Time[i]
        # for x in list_all:
        #     print x,list_all[x]
        # self.Sum_list_all_t = {} #整合数据 >40
        # self.Sum_list_all_f = {}  # 整合数据 <40
        # self.Sum_list_all_no_submit = {}  # 整合数据 <40
        # self.list_all = {}  # 所有数据
        # self.Sun_Data = {}  # 所有统计完成数据
        # for x in Userlist:
        #     self.list_all[x] = []
        # # ---------------------------
        # for filename in self.list_file:  # 文件数量循环
        #     self.soup = BeautifulSoup(open(os.getcwd() + r'\\' + 'data_all' + r'\\' + filename), 'lxml')
        #     td_all = self.soup.findAll("div")[14:]
        #     for x in td_all:  # 删除所有组相关的DIV
        #         if x.get_text().encode("utf-8") in GroupList:
        #             td_all.remove(x)
        #     arrw_name = self.GetPeople(td_all, Userlist)  # 获取每页人员下标
        #     # print "arrw_name is %s" % arrw_name
        #     for x in arrw_name[:-1]:
        #         '''不存在则创建key'''
        #         if td_all[x].get_text().encode("utf-8") in self.list_all.keys():
        #             pass
        #         else:
        #             self.list_all[td_all[x].get_text().encode("utf-8")] = []
        #     self.Pool_Soap(arrw_name, td_all)  # 汇总所有html数据，放入字典中
        #     # self.Sum_Pool_No_Sumbit(arrw_name,td_all) #汇总所有html数据，放入字典中(未提交的数据)
        #     self.Sum_Pool()
        # self.new_report(self.Sun_Data, Group_Info)

class Data_Project():
    '''项目工时处理，非中试人员'''
    def __init__(self):
        if os.path.exists(os.getcwd() + r'\\'+r'Report\report_project.html'):
            os.remove(os.path.abspath(os.getcwd() + r'\\'+ r'Report\report_project.html'))
        #self.soup = BeautifulSoup(open(os.getcwd() + '\Public\data_pro.html'), 'lxml')
        self.soup = BeautifulSoup(open(os.getcwd() + '\data_pro.html'), 'lxml')
        self.soup_new = BeautifulSoup(open(os.getcwd()+ r'\Conf\report_project.html'), 'lxml')

    def Data_People_Time(self,Userlist):
        '''统计项目、编号、部门、人员的工时'''
        arrw_pro,arrw_num,arrw_bran = [],[],[]
        re_arrw_pro, re_arrw_num, re_arrw_bran, arrw_people, list_tmp, list_return, arrw_zero = [], [], [], [], {}, {}, []
        td_all = self.soup.findAll("td")
        for num, i in enumerate(td_all):
            #print num,i.get_text().encode("utf-8")
            '''arrw_pro项目'''
            x = i.get_text().encode("utf-8")
            if num > 4:
                if x == "总计":
                    break
                    #pass
                arrw_pro.append(x)
        for num,a in enumerate(td_all):
            x = a.get_text().encode("utf-8")
            if "汇总：" == x:
                people_end = num
        for xx in range(len(arrw_pro)+6,len(arrw_pro)*2+6):
            '''arrw_num编号'''
            num = td_all[xx].get_text().encode("utf-8")
            arrw_num.append(num)
        for xxxx in range(len(arrw_pro)*2+6,len(arrw_pro)*3+6):
            '''arrw_bran部门'''
            bran = td_all[xxxx].get_text().encode("utf-8")
            arrw_bran.append(bran)
        for s in range(len(arrw_pro)*3+7,people_end):
            x = td_all[s].get_text().encode("utf-8")
            if "KD" in x:
                arrw_people.append(td_all[s+1].get_text().encode("utf-8"))
                #print td_all[s+1].get_text().encode("utf-8")
        begin_point = people_end+4 #起始点
        for x in arrw_people:
            '''人名循环'''
            arrw_tmp = []
            for num_s in range(0, len(arrw_pro)+1):
                '''每个人名循环项目数+1总汇'''
                arrw_tmp.append(td_all[begin_point].get_text().encode("utf-8"))
                begin_point += 1
            list_tmp[x] = arrw_tmp[:-1]
        for x in list_tmp:
            '''list_return过滤符合部门的用户'''
            if x in Userlist:
                pass
            else:
                list_return[x] = list_tmp[x]
        for num in range(0,len(arrw_pro)):
            arrw_zero.append(0)
        for xx in list_return:
            '''计算出哪些列和为0，该列删除'''
            for num2,xxx in enumerate(list_return[xx]):
                arrw_zero[num2] = arrw_zero[num2] + float(xxx)
            print xx,filter(lambda x: x != '0', list_return[xx])
        for num3,value in enumerate(arrw_zero):
            '''按照计算出来的0列，删除head'''
            if value:
                re_arrw_pro.append(arrw_pro[num3])
                re_arrw_num.append(arrw_num[num3])
                re_arrw_bran.append(arrw_bran[num3])
            else:
                for xx in list_return:
                    '''按照计算出来的0列，打标签'''
                    list_return[xx][num3] = "None" #打标签
        for xx in list_return:
            '''清空标签列'''
            # print list_return[xx]
            list_return[xx] = filter(lambda x: x != 'None', list_return[xx])
        return [re_arrw_pro,re_arrw_num,re_arrw_bran,list_return]

    def change_test(self,Obj,value):
        '''更新数据'''
        Obj.string = value

    def Insert_Head(self, tables, values, head_name):
        '''插入表头'''
        tr = self.soup_new.new_tag('tr')
        head = self.soup_new.new_tag('th')
        tables.append(tr)
        tr.insert(0, head)
        head.string = head_name
        for num,x in enumerate(values):
            tmp_head = self.soup_new.new_tag('th')
            tables.append(tmp_head)
            tr.insert(num+1, tmp_head)
            tmp_head.string = x

    def Insert_Body(self, tables, values, body_name):
        '''插入body'''
        tr = self.soup_new.new_tag('tr')
        head = self.soup_new.new_tag('td')
        tables.append(tr)
        tr.insert(0, head)
        head.string = body_name
        for num, x in enumerate(values):
            tmp_head = self.soup_new.new_tag('td')
            tables.append(tmp_head)
            tr.insert(num + 1, tmp_head)
            tmp_head.string = x

    def new_report(self,All_Data):
        '''模板生成新html'''
        table1 = self.soup_new('table')  #获得表
        self.Insert_Head(table1[0], All_Data[0],"项目名称")   #插入项目名称
        self.Insert_Head(table1[0], All_Data[1], "项目编号")  # 插入项目编号
        self.Insert_Head(table1[0], All_Data[2], "产品部门")  # 插入产品部门
        for key in All_Data[3]:
            #print key,All_Data[key]
            self.Insert_Body(table1[0], All_Data[3][key], key)  # 插入项目名称
        sa = open(os.getcwd() + r'\\'+r'Report\report_project.html','w')
        sa.write(str(self.soup_new))
        sa.close()

    def run(self,Userlist,GroupList):
        re_all_data = self.Data_People_Time(Userlist) #计算数据
        for x in re_all_data:
            if x:
                self.new_report(re_all_data) #生成报告
            else:
                raise RuntimeError('Data is hollow')

class Data_V_All():
    '''每周工时处理'''
    def __init__(self):
        # if os.path.exists(os.getcwd() + r'\\'+r'Report\report.html'):
        #     os.remove(os.path.abspath(os.getcwd() + r'\\'+ r'Report\report.html'))
        #self.soup = BeautifulSoup(open(os.getcwd() + r'\\' + 'data_all\data_all_1.html'), 'lxml')
        self.soup_new = BeautifulSoup(open(os.getcwd()+ r'\\' + r'Conf\report_all.html'), 'lxml')
        self.list_file = self.GetDir(os.getcwd() + r'\\' + 'data_all')  # 获取所有文件
        #self.list_file_report = self.GetDir(os.getcwd() + r'\\' + 'Report')  # 获取所有文件

    def is_Chinese(self,word):
        for ch in word.decode('utf-8'):
            if u'\u4e00' <= ch <= u'\u9fff':
                return True
        return False

    def GetPeople(self,td_all,Userlist):
        '''获取用户名'''
        arrw_name = []
        for num, i in enumerate(td_all):
            x = i.get_text().encode("utf-8")
            #print num,x
            if self.is_Chinese(x):
                arrw_name.append(num)
        arrw_name.append(len(td_all))
        return arrw_name

    def GetDir(self, path):
        '''获取该设备所有模块/获取该模块下所有请求'''
        list_dir = []
        dirs = os.listdir(path)
        for i in dirs:
            list_dir.append(i)
        return list_dir

    def Pool_Soap(self,arrw_name,td_all):
        '''汇总所有html数据，放入字典中'''
        for xx in range(0, len(arrw_name) - 1):
            #print td_all[arrw_name[xx]].get_text().encode("utf-8")
            tmp_arr, num = [], 0
            # print arrw_name[xx + 1]
            for xxx in range(arrw_name[xx] + 1, arrw_name[xx + 1]):
                if num == 5:  # 5个清空
                    # print td_all[xxx].get_text().encode("utf-8")
                    self.list_all[td_all[arrw_name[xx]].get_text().encode("utf-8")].append(tmp_arr)
                    tmp_arr, num = [], 0
                tmp_arr.append(td_all[xxx].get_text().encode("utf-8"))
                num += 1
                if xxx == arrw_name[xx + 1] - 1:  # 最后一次
                    self.list_all[td_all[arrw_name[xx]].get_text().encode("utf-8")].append(tmp_arr)
                #print tmp_arr

    def Sum_Pool(self,Userlist):
        '''汇总工时数据'''
        for key in self.list_all:
            if key not in Userlist:
                continue
            tmp_value = 0
            for x in self.list_all[key]:
                for xx in range(3,5):
                    if xx == 2:
                        continue
                    tmp_value += float(x[xx])
            if tmp_value >= 36:
                self.Sum_list_all_t[key] = tmp_value
                if key in self.Sum_list_all_f:
                    self.Sum_list_all_f.pop(key)
            else:
                self.Sum_list_all_f[key] = tmp_value

    def Sum_Pool_No_Sumbit(self,arrw_name,td_all):
        '''汇总工时数据(未提交的数据)'''
        for key in self.list_all:
            tmp_value = 0
            for x in self.list_all[key]:
                tmp_value += float(x[1])
            if tmp_value:
                self.Sum_list_all_no_submit[key] = tmp_value

    def Miss_Time(self,list_s):
        '''统计漏填工时人员'''
        list_tmp = {}
        for key in list_s:
            num = float(list_s[key][1])+float(list_s[key][3])+float(list_s[key][4])
            if num < 7.5 and num !=0:
                list_tmp[key] = num
        return list_tmp

    def Not_Time(self,list_s):
        '''统计未填工时人员'''
        list_tmp = {}
        for key in list_s:
            num = float(list_s[key][1])+float(list_s[key][2])+float(list_s[key][3])+float(list_s[key][4])
            if num == 0:
                list_tmp[key] = num
        return list_tmp

    def Not_Post_Time(self,list_s):
        '''统计未提交工时人员'''
        list_tmp = {}
        for key in list_s:
            num = float(list_s[key][1])
            if num > 0:
                list_tmp[key] = num
        return list_tmp

    def OK_Time(self,list_s):
        '''统计正确工时人员'''
        list_tmp = {}
        for key in list_s:
            num = float(list_s[key][1])+float(list_s[key][3])+float(list_s[key][4])
            if num > 7.5:
                list_tmp[key] = num
        return list_tmp

    def change_test(self,Obj,value):
        '''更新数据'''
        Obj.string = value

    def Insert_Table(self,tables,values):
        '''插入表'''
        new_tr1 = self.soup_new.new_tag('tr')  # 添加tr标签
        new_tr2 = self.soup_new.new_tag('tr')  # 添加tr标签
        tables.append(new_tr1)
        tables.append(new_tr2)
        head = self.soup_new.new_tag('th')
        head2 = self.soup_new.new_tag('td')
        new_tr1.insert(0, head)
        new_tr2.insert(0, head2)
        head.string = '时间/人员'
        #-------------
        today = datetime.date.today()
        oneday = datetime.timedelta(days=1)
        yesterday = today - oneday
        self.Time = str(yesterday)
        head2.string = self.Time
        #------------------
        for num,i in enumerate(values):
            title = self.soup_new.new_tag('th')
            data = self.soup_new.new_tag('td')
            new_tr1.insert(num + 1, title)
            new_tr2.insert(num + 1, data)
            title.string = str(i)
            data.string = str(values[i])

    def Insert_Table_Resule(self, tables, values):
        x_n = len(values) / 4
        #print " x_n is %s" % x_n
        #print "len(values) is %s" % len(values)
        if x_n != 0:
            if len(values)%x_n > 1:
                x_n += 1
        new_tr1 = self.soup_new.new_tag('tr')  # 添加tr标签
        tables.append(new_tr1)
        for x in range(0, x_n):
            td_data1 = self.soup_new.new_tag('th')
            td_data2 = self.soup_new.new_tag('th')
            new_tr1.insert(0, td_data1)
            new_tr1.insert(1, td_data2)
            td_data1.string = "姓名"
            td_data2.string = "汇总工时"

        num = 0
        new_tr1 = self.soup_new.new_tag('tr')  # 添加tr标签
        tables.append(new_tr1)
        for xx in values:
            if num ==x_n*2:
                new_tr1 = self.soup_new.new_tag('tr')  # 添加tr标签
                tables.append(new_tr1)
                num = 0
            td_data = self.soup_new.new_tag('td')
            new_tr1.insert(num, td_data)
            td_data.string = str(xx)
            td_data2 = self.soup_new.new_tag('td')
            new_tr1.insert(num+1, td_data2)
            td_data2.string = str(values[xx])
            num += 2

    def new_report(self,list_data_t,list_data_f,list_data_no_sumbit):
        '''模板生成新html'''
        table1 = self.soup_new('table')  #获得表
        #print Miss_Time
        # self.Insert_Table(table1[0], Miss_Time)  # 插入漏填工时表
        # self.Insert_Table(table1[1], Not_Time)  # 插入未填工时表
        # self.Insert_Table(table1[2], Not_Post_Time)  # 插入未提交工时表
        # self.Insert_Table(table1[3], OK_Time)  #插入正确工时表
        self.Insert_Table_Resule(table1[0], list_data_t) #插入明细表>40
        self.Insert_Table_Resule(table1[1], list_data_f)  # 插入明细表<40
        self.Insert_Table_Resule(table1[2], list_data_no_sumbit)  # 插入明细表<40
        sa = open(os.getcwd() + r'\\'+r'Report\report_data_all.html','w')
        sa.write(str(self.soup_new))
        sa.close()

    def run(self,Userlist,GroupList):
        self.list_all = {} #所有数据
        self.Sum_list_all_t = {} #整合数据 >40
        self.Sum_list_all_f = {}  # 整合数据 <40
        self.Sum_list_all_no_submit = {}  # 整合数据 <40
        for x in Userlist:
            self.list_all[x] = []
        #---------------------------
        for filename in self.list_file:
            self.soup = BeautifulSoup(open(os.getcwd() + r'\\' + 'data_all'+ r'\\'+filename), 'lxml')
            td_all = self.soup.findAll("div")[14:]
            for x in td_all:
                if x.get_text().encode("utf-8") in GroupList:
                    td_all.remove(x)
            arrw_name = self.GetPeople(td_all,Userlist) #获取人员所在下标
            #print arrw_name
            for x in arrw_name[:-1]:
                '''不存在conf中,则新建'''
                if td_all[x].get_text().encode("utf-8") in self.list_all.keys():
                    pass
                else:
                    self.list_all[td_all[x].get_text().encode("utf-8")] = []
            self.Pool_Soap(arrw_name,td_all) #汇总所有html数据，放入字典中
            self.Sum_Pool_No_Sumbit(arrw_name,td_all) #汇总所有html数据，放入字典中(未提交的数据)
            self.Sum_Pool(Userlist)
        for x in self.Sum_list_all_t:
            print x,self.Sum_list_all_t[x]
        print"---"*20
        for x in self.Sum_list_all_f:
            print x,self.Sum_list_all_f[x]
            # for x in self.Sum_list_all:
            #     print x,self.Sum_list_all[x]
        # for x in self.list_all:
        #     print x,self.list_all[x]
        self.new_report(self.Sum_list_all_t,self.Sum_list_all_f,self.Sum_list_all_no_submit)


class Data_V_Month():
    '''每月工时处理'''
    def __init__(self):
        # if os.path.exists(os.getcwd() + r'\\'+r'Report\report.html'):
        #     os.remove(os.path.abspath(os.getcwd() + r'\\'+ r'Report\report.html'))
        #self.soup = BeautifulSoup(open(os.getcwd() + r'\\' + 'data_all\data_all_1.html'), 'lxml')
        self.soup_new = BeautifulSoup(open(os.getcwd()+ r'\\' + r'Conf\report_month.html'), 'lxml')
        self.list_file = self.GetDir(os.getcwd() + r'\\' + 'data_all')  # 获取所有文件
        #self.list_file_report = self.GetDir(os.getcwd() + r'\\' + 'Report')  # 获取所有文件

    def In_Ch_Obj(self,Obj_D,Pop,Sort="th",String=u"姓名"):
        Obj_In = self.soup_new.new_tag(Sort)
        Obj_In.string = String
        Obj_D.insert(Pop, Obj_In)

    def is_Chinese(self,word):
        for ch in word.decode('utf-8'):
            if u'\u4e00' <= ch <= u'\u9fff':
                return True
        return False

    def GetPeople(self,td_all,Userlist):
        '''获取用户名'''
        arrw_name = []
        for num, i in enumerate(td_all):
            x = i.get_text().encode("utf-8")
            if self.is_Chinese(x):
                arrw_name.append(num)
        arrw_name.append(len(td_all))
        return arrw_name

    def GetDir(self, path):
        '''获取该设备所有模块/获取该模块下所有请求'''
        list_dir = []
        dirs = os.listdir(path)
        for i in dirs:
            list_dir.append(i)
        return list_dir

    def Pool_Soap(self,arrw_name,td_all):
        '''汇总所有html数据，放入字典中'''
        for xx in range(0, len(arrw_name) - 1):
            #print td_all[arrw_name[xx]].get_text().encode("utf-8")
            tmp_arr, num = [], 0
            # print arrw_name[xx + 1]
            for xxx in range(arrw_name[xx] + 1, arrw_name[xx + 1]):
                if num == 5:  # 5个清空
                    # print td_all[xxx].get_text().encode("utf-8")
                    self.list_all[td_all[arrw_name[xx]].get_text().encode("utf-8")].append(tmp_arr)
                    tmp_arr, num = [], 0
                tmp_arr.append(td_all[xxx].get_text().encode("utf-8"))
                num += 1
                if xxx == arrw_name[xx + 1] - 1:  # 最后一次
                    self.list_all[td_all[arrw_name[xx]].get_text().encode("utf-8")].append(tmp_arr)
                #print tmp_arr

    def Sum_Pool(self):
        '''汇总工时数据'''
        for key in self.list_all:
            tmp_value = 0
            for x in self.list_all[key]:
                for xx in range(3,5):
                    # if xx == 2:
                    #     continue
                    tmp_value += float(x[xx])
            #print key,tmp_value
            self.Sun_Data[key] = tmp_value

    def Miss_Time(self,list_s):
        '''统计漏填工时人员'''
        list_tmp = {}
        for key in list_s:
            num = float(list_s[key][1])+float(list_s[key][3])+float(list_s[key][4])
            if num < 7.5 and num !=0:
                list_tmp[key] = num
        return list_tmp

    def Not_Time(self,list_s):
        '''统计未填工时人员'''
        list_tmp = {}
        for key in list_s:
            num = float(list_s[key][1])+float(list_s[key][2])+float(list_s[key][3])+float(list_s[key][4])
            if num == 0:
                list_tmp[key] = num
        return list_tmp

    def Not_Post_Time(self,list_s):
        '''统计未提交工时人员'''
        list_tmp = {}
        for key in list_s:
            num = float(list_s[key][1])
            if num > 0:
                list_tmp[key] = num
        return list_tmp

    def OK_Time(self,list_s):
        '''统计正确工时人员'''
        list_tmp = {}
        for key in list_s:
            num = float(list_s[key][1])+float(list_s[key][3])+float(list_s[key][4])
            if num > 7.5:
                list_tmp[key] = num
        return list_tmp

    def change_test(self,Obj,value):
        '''更新数据'''
        Obj.string = value

    def Insert_Table(self,tables,values):
        '''插入表'''
        new_tr1 = self.soup_new.new_tag('tr')  # 添加tr标签
        new_tr2 = self.soup_new.new_tag('tr')  # 添加tr标签
        tables.append(new_tr1)
        tables.append(new_tr2)
        head = self.soup_new.new_tag('th')
        head2 = self.soup_new.new_tag('td')
        new_tr1.insert(0, head)
        new_tr2.insert(0, head2)
        head.string = '时间/人员'
        #-------------
        today = datetime.date.today()
        oneday = datetime.timedelta(days=1)
        yesterday = today - oneday
        self.Time = str(yesterday)
        head2.string = self.Time
        #------------------
        for num,i in enumerate(values):
            title = self.soup_new.new_tag('th')
            data = self.soup_new.new_tag('td')
            new_tr1.insert(num + 1, title)
            new_tr2.insert(num + 1, data)
            title.string = str(i)
            data.string = str(values[i])

    def Insert_Table_Resule(self, Table, Data, Info):
        n = 1
        new_tr1 = self.soup_new.new_tag('tr')  # 添加tr标签
        td_data1 = self.soup_new.new_tag('th')
        td_data1.string = "所在组"
        new_tr1.insert(0, td_data1)
        for x8 in range(1, n * 2 + 1, 2): #加入表头
            self.In_Ch_Obj(Sort="th", Obj_D=new_tr1, Pop=x8, String="姓名")
            self.In_Ch_Obj(Sort="th", Obj_D=new_tr1, Pop=x8 + 1, String="工时")
        Table.append(new_tr1)
        ###################################报告初始化完成#########################################
        for x1 in Data:
            for x2 in Info:
                if x1 in Info[x2].keys():
                    Info[x2][x1] = Data[x1]
        ###################################统计数据Info更新######################
        print Info
        for ee in Info:
            Info[ee] = sorted(Info[ee].items(),key = lambda x:x[1],reverse = True)
        print Info
        for x3 in Info:
            # print sorted(Info[x3].items(),key = lambda x:x[1],reverse = True)
            #keys_I = Info[x3].keys()
            Y = len(Info[x3]) / n
            YY = len(Info[x3]) % n
            if (YY != 0) and (Y == 0): #不止一行并且不是整数行
                Y = 1
            elif (Y != 0) and (YY !=0):
                Y += 1
            elif (Y!=0) and(YY ==0):
                pass
            else:
                raise RuntimeError('Data is hollow')
            count = 0
            for x5 in range(0, Y):  # 行数循环
                if (count+n) < len(Info[x3]):  # 未超出最大长度
                    new_tr1 = self.soup_new.new_tag('tr')  # 添加tr标签
                    self.In_Ch_Obj(Sort="td", Obj_D=new_tr1, Pop=0, String=x3)
                    for z1 in range(1,n*2+1,2):
                        self.In_Ch_Obj(Sort="td", Obj_D=new_tr1, Pop=z1, String=Info[x3][count][0])
                        self.In_Ch_Obj(Sort="td", Obj_D=new_tr1, Pop=z1+1, String=str(Info[x3][count][1]))
                        count +=1
                    Table.append(new_tr1)
                else:
                    new_tr2 = self.soup_new.new_tag('tr')  # 添加tr标签
                    self.In_Ch_Obj(Sort="td", Obj_D=new_tr2, Pop=0, String=x3)
                    for z1 in range(1,(len(Info[x3])-count)*2+1,2):
                        self.In_Ch_Obj(Sort="td", Obj_D=new_tr2, Pop=z1, String=Info[x3][count][0])
                        self.In_Ch_Obj(Sort="td", Obj_D=new_tr2, Pop=z1+1, String=str(Info[x3][count][1]))
                        count +=1
                    Table.append(new_tr2)

    def new_report(self,list_data,Group_Info):
        '''模板生成新html'''
        table1 = self.soup_new('table')  #获得表
        self.Insert_Table_Resule(table1[0], list_data,Group_Info) #插入明细表>40
        sa = open(os.getcwd() + r'\\'+r'Report\report_data_month.html','w')
        sa.write(str(self.soup_new))
        sa.close()

    def run(self,Userlist,GroupList,Group_Info):
        self.list_all = {} #所有数据
        self.Sun_Data = {} #所有统计完成数据
        for x in Userlist:
            self.list_all[x] = []
        #---------------------------
        for filename in self.list_file:
            self.soup = BeautifulSoup(open(os.getcwd() + r'\\' + 'data_all'+ r'\\'+filename), 'lxml')
            td_all = self.soup.findAll("div")[14:]
            for x in td_all:
                if x.get_text().encode("utf-8") in GroupList:
                    td_all.remove(x)
            arrw_name = self.GetPeople(td_all,Userlist) #获取每页所有查询出来的人员下标
            #print "arrw_name is %s" % arrw_name
            for x in arrw_name[:-1]:
                '''不存在则创建key'''
                if td_all[x].get_text().encode("utf-8") in self.list_all.keys():
                    pass
                else:
                    self.list_all[td_all[x].get_text().encode("utf-8")] = []
            self.Pool_Soap(arrw_name,td_all) #汇总所有html数据，放入字典中
            #self.Sum_Pool_No_Sumbit(arrw_name,td_all) #汇总所有html数据，放入字典中(未提交的数据)
            self.Sum_Pool()
        self.new_report(self.Sun_Data,Group_Info)

if __name__ == "__main__":
    PI = Pruduct_ini.Pro_Ini('../Conf/conf.ini')
    UserList = PI.GetUserList() #检测人员
    GroupList = PI.GetUserGroup()
    #Data_Project().run(UserList,GroupList)
    Data_V_All().run(UserList, GroupList)  # 跑处理返回数据
    # for num,i in enumerate(td_all[2:-7]):
    #     print num,i.get_text()
        # if num in [1,2,3,4,5,6]:
        #     list_title.append(td_all[num])
