#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os,sys
from Public.Pruduct_ini import Pro_Ini
from Public.Get_TIme_Work import Selenium_Oa_Project
from Public.Script_Pro import Data_Project
from Public.Get_TIme_Work import Selenium_Oa_Month
from Public.Script_Pro import Data_V_Month
from Public.Get_TIme_Work import Selenium_Oa
from Public.Script_Pro import Data_V
from Public.Get_TIme_Work import Selenium_Oa_week
from Public.Script_Pro import Data_V_All


# if sys.argv[1] == "every_day":
#     '''每日中试工时检查'''
#     PI = Pro_Ini(os.getcwd() + '//' + 'Conf/conf.ini')
#     User = PI.GetUserName()  # 登录用户名
#     Userlist = PI.GetUserList()  # 获取用户列表
#     GroupList = PI.GetUserGroup()  # 获取用户组
#     GroupListInfo = PI.GetUserGroup_Con()  # 获取用户和组关系
#     Selenium_Oa(User).run()  # 跑selenium
#     Data_V().run(Userlist, GroupList, GroupListInfo)  # 跑处理返回数据
# elif sys.argv[1] == "every_week":
#     '''每周中试工时检查'''
#     def GetDir():
#         '''获取该设备所有模块/获取该模块下所有请求'''
#         path = os.getcwd() + r'\\' + 'data_all'
#         list_dir = []
#         dirs = os.listdir(path)
#         for i in dirs:
#             list_dir.append(i)
#         for x in list_dir:
#             os.remove(os.getcwd() + '\data_all' + '\\' + x)
#     GetDir()
#     PI = Pro_Ini(os.getcwd() + '//' + 'Conf/conf.ini')
#     User = PI.GetUserName()  # 登录用户名
#     Userlist = PI.GetUserList()  # 获取用户列表
#     GroupList = PI.GetUserGroup()  # 获取用户组
#     Selenium_Oa_week(User,day=7).run()  # 跑selenium
#     Data_V_All().run(Userlist, GroupList)  # 跑处理返回数据
# elif sys.argv[1] == "every_week_14":
#     '''每周中试工时检查1-4'''
#     def GetDir():
#         '''获取该设备所有模块/获取该模块下所有请求'''
#         path = os.getcwd() + r'\\' + 'data_all'
#         list_dir = []
#         dirs = os.listdir(path)
#         for i in dirs:
#             list_dir.append(i)
#         for x in list_dir:
#             os.remove(os.getcwd() + '\data_all' + '\\' + x)
#     GetDir()
#     PI = Pro_Ini(os.getcwd() + '//' + 'Conf/conf.ini')
#     User = PI.GetUserName()  # 登录用户名
#     Userlist = PI.GetUserList()  # 获取用户列表
#     GroupList = PI.GetUserGroup()  # 获取用户组
#     Selenium_Oa_week(User,day=4).run()  # 跑selenium
#     Data_V_All().run(Userlist, GroupList)  # 跑处理返回数据
# elif sys.argv[1] == "every_month":
#     '''每月中试工时检查'''
#     PI = Pro_Ini(os.getcwd() + '//' + 'Conf/conf.ini')
#     User = PI.GetUserName()  # 登录用户名
#     Userlist = PI.GetUserList()  # 获取用户列表
#     GroupList = PI.GetUserGroup()  # 获取用户组
#     GroupListInfo = PI.GetUserGroup_Con()  # 获取用户和组关系
#     Selenium_Oa_Month(User).run()  # 跑selenium
#     Data_V_Month().run(Userlist, GroupList, GroupListInfo)  # 跑处理返回数据
# elif sys.argv[1] == "every_project":
#     '''非中试项目人员工时检查'''
#     PI = Pro_Ini(os.getcwd() + '//' + 'Conf/conf.ini')
#     User = PI.GetUserName()  # 登录用户名
#     Userlist = PI.GetUserList()  # 获取用户列表
#     GroupList = PI.GetUserGroup()  # 获取用户组
#     Selenium_Oa_Project(User).run()  # 跑selenium
#     Data_Project().run(Userlist, GroupList)  # 跑处理返回数据
def GetDir():
    '''获取该设备所有模块/获取该模块下所有请求'''
    path = os.getcwd() + r'\\' + 'data_all'
    list_dir = []
    dirs = os.listdir(path)
    for i in dirs:
        list_dir.append(i)
    for x in list_dir:
        os.remove(os.getcwd() + '\data_all' + '\\' + x)

PI = Pro_Ini(os.getcwd() + '//' + 'Conf/conf.ini') #配置文件
User = PI.GetUserName()  # 登录用户名
Userlist = PI.GetUserList()  # 获取用户列表
GroupList = PI.GetUserGroup()  # 获取用户组
GroupListInfo = PI.GetUserGroup_Con()  # 获取用户和组关系
GetDir()
if __name__ == "__main__":
    model = sys.argv[1]
    print model
    #model = "every_day"
    if model == "every_day":
        Selenium_Oa(User).run()  # 跑selenium
        Data_V().run(Userlist, GroupList, GroupListInfo)  # 跑处理返回数据
    elif model == "every_week":
        print "every_week"
        Selenium_Oa_week(User,day=7).run()  # 跑selenium
        Data_V_All().run(Userlist, GroupList)  # 跑处理返回数据
    elif model == "every_week_14":
        Selenium_Oa_week(User,day=4).run()  # 跑selenium
        Data_V_All().run(Userlist, GroupList)  # 跑处理返回数据
    elif model == "every_month":
        Selenium_Oa_Month(User).run()  # 跑selenium
        Data_V_Month().run(Userlist, GroupList, GroupListInfo)  # 跑处理返回数据
    elif model == "every_project":
        Selenium_Oa_Project(User).run()  # 跑selenium
        Data_Project().run(Userlist, GroupList)  # 跑处理返回数据