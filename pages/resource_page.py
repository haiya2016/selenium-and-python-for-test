# coding=utf-8
'''
Created on 2018-9-9
@author: wjx
Project:资源实例页面
'''
from selenium.webdriver.common.by import By
from base_page import BasePage


class ResoucePage(BasePage):
    '''
    继承BasePage类
    '''
    vmsTab_loc = (By.ID, 'vmsTab')                          # 云主机
    storagesTab_loc = (By.ID, 'storagesTab')                # 云硬盘
    objectStoragesTab_loc = (By.ID, 'objectStoragesTab')    # 对象存储
    databaseTab_loc = (By.ID, 'databaseTab')                # 数据库
    publicipsTab_loc = (By.ID, 'publicipsTab')              # 公网IP
    sshkeysTab_loc = (By.ID, 'sshkeysTab')                  # SSH密钥
    taskTab_loc = (By.ID, 'taskTab')                        # 调度任务
