#coding=utf-8
import ConfigParser
import os

class Pro_Ini():
    '''获取ini文件信息'''
    def __init__(self,path):
        self.path = path
        self.cf = ConfigParser.ConfigParser()
        self.cf.read(self.path)
    def GetUserName(self):
        '''登陆用户名密码'''
        UserName = self.cf.get("User","name")
        UserPasswd = self.cf.get("User","passwd")
        return [UserName,UserPasswd]
    def GetUserList(self):
        '''实习生名单'''
        list_name = []
        list_group = self.GetUserGroup()
        for x in list_group:
            for key in self.cf.items(x):
                list_name.append(key[1])
        return list_name
    def GetUserGroup(self):
        '''人员组名单'''
        list_name = []
        for key in self.cf.items("Group"):
            list_name.append(key[1])
        return list_name

    def GetUserGroup_Con(self):
        '''人员和组关系'''
        list_name = {}
        list_group = self.GetUserGroup()
        for x in list_group:
            tmplist = {}
            for key in self.cf.items(x):
                tmplist[key[1]]= 0
            list_name[x] = tmplist
        return list_name


if __name__ == "__main__":
    P = Pro_Ini('../Conf/conf.ini')
    print P.GetUserList()