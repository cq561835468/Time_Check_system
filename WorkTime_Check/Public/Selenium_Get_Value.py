#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import Pruduct_ini
import time

class Selenium_Oa():
    def __init__(self):
        options = webdriver.FirefoxOptions()
        options.set_headless()
        self.driver = webdriver.Firefox(firefox_options=options)
        self.driver.maximize_window()

    def Go_To_Page(self):
        self.driver.get("https://sso.kedacom.com:8443/CasServer/login")
        self.driver.find_element_by_id("ui_username").send_keys(User[0])
        self.driver.find_element_by_id("ui_password").send_keys(User[1])
        self.driver.find_element_by_class_name("btn").click()
        self.driver.get("https://oa.kedacom.com/report/platform/console/main.do")
        arrw_inner = self.driver.find_elements_by_class_name("l-accordion-header-inner")
        arrw_inner[1].click()
        arrw_span = self.driver.find_elements_by_tag_name('span')
        arrw_span[4].click()

    def Select_All(self):
        '''测试部选择'''
        self.driver.find_element_by_class_name("fr-trigger-center").click()
        time.sleep(2)
        arrw_plus = self.driver.find_elements_by_class_name("fr-tree-elbow-end-plus")
        arrw_plus[0].click()
        time.sleep(2)
        arrw_plus = self.driver.find_elements_by_class_name("fr-tree-elbow-plus")
        arrw_plus[2].click()
        time.sleep(2)
        arrw_plus = self.driver.find_elements_by_class_name("fr-tree-elbow-plus")
        arrw_plus[2].click()
        time.sleep(2)
        arrw_span = self.driver.find_elements_by_tag_name("span")
        # for num,i in enumerate(arrw_span):
        #     print num,i.text
        arrw_span[27].click()

    def Time_Set(self):
        '''起始时间、结束时间点击'''
        arrw_trigger = self.driver.find_elements_by_class_name("fr-date-trigger-center")
        arrw_trigger[0].click()
        arrw_day = self.driver.find_elements_by_class_name("day")
        date_time = time.strftime("%d")
        for num,i in enumerate(arrw_day):
            if str(int(date_time)-1) == i.text.encode("utf-8"):
                 i.click()

        arrw_trigger[1].click()
        arrw_day = self.driver.find_elements_by_class_name("day")
        date_time = time.strftime("%d")
        for num,i in enumerate(arrw_day):
            if str(int(date_time)-1) == i.text.encode("utf-8"):
                 i.click()

    def Select_Click(self):
        '''点击查询'''
        arrw_button = self.driver.find_elements_by_class_name("fr-btn-text")
        arrw_button[1].click()

    def OutPut_Excel(self):
        '''导出工时数据'''
        #arrw_day = self.driver.find_elements_by_class_name("fr-btn-arrrow")
        arrw_button = self.driver.find_elements_by_tag_name("<table")
        arrw_button[9].click()
        print arrw_button[9].text
        #for num,sa in enumerate(arrw_button):
            # print num,sa.text
            # if sa.text.encode("utf-8") == '输出':
            #sa.click()

    def run(self,User):
        '''主函数'''
        self.Go_To_Page()  #进入工时页面
        time.sleep(3)
        self.driver.switch_to.frame("kdUIFrameWindow")
        print self.driver.page_source
        self.Select_All() #选择测试部
        self.Time_Set() #选择工时
        self.Select_Click() #点击查询
        self.OutPut_Excel() #导出工时


if __name__ == "__main__":
    PI = Pruduct_ini.Pro_Ini('../Conf/conf.ini')
    User = PI.GetUserName() #登录用户名
    De = Selenium_Oa().run(User)