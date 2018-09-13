# coding=utf-8
'''
Created on 2018-9-9
@author: wjx
Project:页面基本操作方法：如open，input_username，input_password，click_submit
'''
from selenium.webdriver.common.by import By
from base_page import BasePage

class LoginPage(BasePage):
    '''
    继承BasePage类
    封装登录页面所需要使用的方法
    '''# 定位器，通过元素属性定位元素对象
    username_loc = (By.NAME, 'username')
    password_loc = (By.NAME, 'password')
    submit_loc = (By.NAME, 'submit')
    usertype_local_loc = (By.XPATH, '//*[@id="userType"]/option[1]')
    usertype_ad_loc = (By.ID, 'adUser')
    msg_loc = (By.XPATH, '//*[@id="cas"]/div/div[1]/div/div[2]/div[2]/div[3]')
    userid_loc = (By.XPATH, '//*[@id="header"]/div[2]/ul/li[5]/a/span')

    # 操作
    # 通过继承覆盖（Overriding）方法：如果子类和父类的方法名相同，优先用子类自己的方法。
    # 打开网页
    # def open(self):
    # # 调用page中的_open打开连接
    #     self._open(self.base_url, self.pagetitle)
    def input_username(self, username):
        '''输入用户名：调用send_keys对象，输入用户名'''
#        self.find_element(*self.username_loc).clear()
        self.find_element(*self.username_loc).send_keys(username)

    def input_password(self, password):
        '''输入密码：调用send_keys对象，输入密码'''
        # self.find_element(*self.password_loc).clear()
        self.find_element(*self.password_loc).send_keys(password)

    def click_submit(self):
        '''点击登录'''
        self.find_element(*self.submit_loc).click()

    def show_msg(self):
        '''用户名或密码不合理时Tip框内容展示'''
        return self.find_element(*self.msg_loc).text

    def swich_usertype(self):
        '''切换为Ad用户登陆'''
        self.find_element(*self.usertype_ad_loc).click()

    def show_userid(self):
        '''登录成功页面中的用户ID查找'''
        return self.find_element(*self.userid_loc).text
        