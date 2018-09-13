# coding=utf-8
'''
Created on 2018-9-9
@author: wjx
Project: 首页模块的测试用例
'''
import unittest
# import sys
# import os
import pymysql
from selenium import webdriver
from BeautifulReport import BeautifulReport
# sys.path.append(os.path.abspath(os.path.dirname(__file__)+'\\'+'..\\pages'))
from pages.login_page import LoginPage
from pages.home_page import HomePage


class HomepageCSC(unittest.TestCase):
    '''
    CSC首页case
    '''

    def setUp(self):
        self.url = 'https://192.168.219.227:8099/csc/index.html'
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.driver.set_window_size(1366, 768)
        self.database = pymysql.connect(
            host='192.168.219.227',
            port=3306,
            user='csc',
            password='csc',
            db='csc')

    def login(self):
        '''
        账号正常登录后返回浏览器给用例使用
        '''
        loginpage = LoginPage(self.driver, self.url, 'WinCloud统一认证平台')
        loginpage.open()
        loginpage.input_username('admin')
        loginpage.input_password('1234567890')
        loginpage.click_submit()
        return self.driver

    def test_switch_dc(self):
        '''切换数据中心'''
        homepage = HomePage(self.login(), self.url, 'WinCloud-CSC')
        # 选择某个数据中心的数据
        homepage.dc_select('DC-PVC')
        print(homepage.dc_check())
        print(homepage.db_check(self.database, 'DC-PVC'))

    def tearDown(self):
        self.driver.close()
        self.database.close()


if __name__ == '__main__':
    TEST_SUITE = unittest.defaultTestLoader.discover(
        r'.\testcase', pattern='*_homepage.py')
    RESULT = BeautifulReport(TEST_SUITE)
    RESULT.report(filename='CSC7.0自动化测试报告_首页',
                  description='首页模块测试报告',
                  log_path='report')
