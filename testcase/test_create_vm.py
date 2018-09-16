# coding=utf-8
'''
Created on 2018-9-9
@author: wjx
Project: 首页模块的测试用例
'''
import unittest
# import sys
# import os
import time
# import pymysql
from selenium import webdriver
from BeautifulReport import BeautifulReport
# sys.path.append(os.path.abspath(os.path.dirname(__file__)+'\\'+'..\\pages'))
from pages.login_page import LoginPage
# from login_page import LoginPage
from pages.vm_create_page import VmCreatePage


class CreateVM(unittest.TestCase):
    '''
    创建云主机case
    '''

    def setUp(self):
        self.url = 'https://192.168.219.227:8099/csc/index.html'
        self.create_vm_url = f'{self.url}#pages/resources/instances/vms/vm_create?previousPage=1'
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.driver.set_page_load_timeout(60)
        self.driver.set_window_size(1366, 768)
        # 调用LoginPage的类方法，直接获取一个已登录的浏览器
        self.login_driver = LoginPage.login(self.driver, self.url, 'admin', '1234567890')
        # self.database = pymysql.connect(
        #     host='192.168.219.227',
        #     port=3306,
        #     user='csc',
        #     password='csc',
        #     db='csc')


    def test_create_vm(self):
        '''切换数据中心'''
        # 使用已登录的浏览器生成一个已登录的云主机创建页面的对象
        vm_page = VmCreatePage(self.login_driver, self.create_vm_url)
        vm_page.open()
        # 设置需要填写的值
        input_items = {
            '云主机名称':'python01',
            'VM Name':'python01',
            'Hostname':'python01',
            '归属服务':'zhh',
            '归属VDC':'zhhvdca',
            '归属用户':'admin',
            '业务系统':'',
            '应用集群':'',
            '到期时间':'2019-01-01',
            '备注':'自动化创建的云主机',
            '可用分区':'AZ-Winserver 虚拟化:WinServer',
            '镜像':'win2012',
            '宿主机':'192.168.206.76',
            '存储池':'Local storage(192.168.206.76)',
            'CPU':'1',
            '内存':'1',
            '系统盘':'',
            'IP池':'208',
        }
        for item in input_items:
            vm_page.input_item(item, input_items[item])
            # time.sleep(2)
        time.sleep(5)

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
