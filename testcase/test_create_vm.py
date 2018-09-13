# coding=utf-8
'''
Created on 2018-9-9
@author: wjx
Project: 首页模块的测试用例
'''
import unittest
import sys
import os
import time
# import pymysql
from selenium import webdriver
from BeautifulReport import BeautifulReport
sys.path.append(os.path.abspath(os.path.dirname(__file__)+'\\'+'..\\pages'))
from login_page import LoginPage
from vm_create_page import VmCreatePage


class CreateVM(unittest.TestCase):
    '''
    创建云主机case
    '''

    def setUp(self):
        self.url = 'https://192.168.219.227:8099/csc/index.html'
        self.create_vm_url = 'https://192.168.219.227:8099/csc/index.html#pages/resources/instances/vms/vm_create?previousPage=1'
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.driver.set_window_size(1366, 768)
        # self.database = pymysql.connect(
        #     host='192.168.219.227',
        #     port=3306,
        #     user='csc',
        #     password='csc',
        #     db='csc')

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

    def test_create_vm(self):
        '''切换数据中心'''
        vmcreatepage = VmCreatePage(self.login(), self.create_vm_url, 'WinCloud-CSC')
        # time.sleep(3)
        vmcreatepage.open()
        time.sleep(3)
        # 选择某个数据中心的数据
        vmcreatepage.input_item('归属服务', 'zhh')
        # time.sleep(5)

    def tearDown(self):
        self.driver.close()
        # self.database.close()


if __name__ == '__main__':
    TEST_SUITE = unittest.defaultTestLoader.discover(
        r'.\testcase', pattern='test_create_vm.py')
    RESULT = BeautifulReport(TEST_SUITE)
    RESULT.report(filename='CSC7.0自动化测试报告_云主机创建',
                  description='云主机创建模块测试报告',
                  log_path='report')
