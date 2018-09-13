# coding=utf-8
'''
Created on 2018-9-9
@author: wjx
Project: 登录模块的测试用例
'''
import unittest
import sys
import os
from selenium import webdriver
from parameterized import parameterized
from BeautifulReport import BeautifulReport
sys.path.append(os.path.abspath(os.path.dirname(__file__)+'\\'+'..\\pages'))
from login_page import LoginPage



class LoginCSC(unittest.TestCase):
    """
          登录CSC的case
    """
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.driver.set_window_size(1366, 768)
        self.url = "https://192.168.219.227:8099/csc/index.html"

    # 使用多组数据进行用例执行
    @parameterized.expand([
        ("user_null", '', 'password', '账号不能为空！'),
        ("pwd_null", 'admin', '', '密码不能为空！'),
        ("local_login", 'admin', '1234567890', 'admin'),
        ("ad_login", 'wjx', 'Admin123', 'wjx')
    ])
    def test_login_csc(self, casename, username, password, asserts):
        '''
        测试使用不同的账号密码组合进行登陆测试
        '''
        login_page = LoginPage(self.driver, self.url)   # 创建一个登陆页面的实例
        login_page.open()
        login_page.input_username(username)
        login_page.input_password(password)

        if casename == 'ad_login':             # 是否切换Ad域登录
            login_page.swich_usertype()
        login_page.click_submit()

        if login_page.on_page('WinCloud-CSC'):  # 判断登陆情况和tip信息
            self.assertEqual(login_page.show_userid(), asserts, "登录的账号与期望不一致")
        else:
            self.assertEqual(login_page.show_msg(), asserts, "提示语与预期不一致")

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    TEST_SUITE = unittest.defaultTestLoader.discover(r'.\testcase', pattern='test_login.py')
    RESULT = BeautifulReport(TEST_SUITE)
    RESULT.report(filename='CSC7.0自动化测试报告_登录', description='登录模块测试报告', log_path='report')
    