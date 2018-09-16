# coding=utf-8
'''
Created on 2018-9-9
@author: wjx
Project:页面基本操作方法：如open，input_username，input_password，click_submit
'''
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.logging_sys import Logger

class LoginPage(BasePage):
    '''
    继承BasePage类
    封装登录页面所需要使用的方法
    '''
    # 定位器，通过元素属性定位元素对象
    username_loc = (By.NAME, 'username')
    password_loc = (By.NAME, 'password')
    submit_loc = (By.NAME, 'submit')
    usertype_local_loc = (By.XPATH, '//*[@id="userType"]/option[1]')
    usertype_ad_loc = (By.ID, 'adUser')
    msg_loc = (By.XPATH, '//*[@id="cas"]/div/div[1]/div/div[2]/div[2]/div[3]')
    userid_loc = (By.XPATH, '//*[@id="header"]/div[2]/ul/li[5]/a/span')

    # 日志
    log = Logger('登录').getlog()

    # 操作
    def input_username(self, username):
        '''输入用户名'''
        self.log.info(f'输入用户名：{username}')
        self.find_element(*self.username_loc).send_keys(username)

    def input_password(self, password):
        '''输入密码'''
        self.log.info(f'输入密码：{password}')
        self.find_element(*self.password_loc).send_keys(password)

    def click_submit(self):
        '''点击登录'''
        self.log.info('点击登录按钮')
        self.find_element(*self.submit_loc).click()

    def show_msg(self):
        '''用户名或密码不合理时Tip框内容展示'''
        mesg = self.find_element(*self.msg_loc).text
        self.log.info(f'提示信息：{mesg}')
        return mesg

    def switch_usertype(self):
        '''切换为AD用户登陆'''
        self.log.info('切换为AD用户登陆')
        self.find_element(*self.usertype_ad_loc).click()

    def show_userid(self):
        '''登录成功页面中的用户ID查找'''
        return self.find_element(*self.userid_loc).text


    @classmethod
    def login(cls, driver, url, username, password, usertype='本地'):
        '''
        类方法：账号正常登录后返回浏览器给用例使用
        '''
        login = cls(driver, url)    # 初始化
        login.open()
        login.input_username(username)
        login.input_password(password)
        if usertype != '本地':
            login.switch_usertype()
        login.click_submit()
        if username == cls.show_userid(login):
            cls.log.info('登录成功')
        else:
            raise AssertionError
        return login.driver
        