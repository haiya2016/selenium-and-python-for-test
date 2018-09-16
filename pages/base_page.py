# coding=utf-8
'''
Created on 2018-9-9
@author: wjx
Project:基础类BasePage，封装所有页面都公用的方法，
定义open函数，重定义find_element，switch_frame，send_keys等函数。
在初始化方法中定义驱动driver，基本url，title
WebDriverWait提供了显式等待方式。
'''
# import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from config.logging_sys import Logger


class BasePage(object):
    """
    BasePage封装所有页面都公用的方法，例如driver, url ,FindElement等
    初始化driver、url、pagetitle等
    """

    def __init__(self, selenium_driver, base_url):
        self.driver = selenium_driver
        self.base_url = base_url
        self.log = Logger('基本操作').getlog()

    def on_page(self, pagetitle):
        '''使用title获取当前窗口title，检查输入的title是否在当前title中，返回比较结果（True 或 False）'''
        return pagetitle in self.driver.title

    def _open(self, url):
        '''打开页面，并校验页面链接是否加载正确
        以单下划线_开头的方法，在使用import *时，该方法不会被导入，保证该方法为类私有的。'''
        self.driver.get(url)
        # print('打开网页：', url)
        # time.sleep(3)
        # self.driver.implicitly_wait(10)
        # self.driver.set_page_load_timeout(60)
        self.driver.refresh()   # 页面打开之后刷新一下，保证js都执行完成
        # assert self.on_page(pagetitle), "打开开页面失败 %s" %url

    def open(self):
        '''定义open方法，调用_open()进行打开链接'''
        self.log.info(f'打开页面：{str(self.base_url)}')
        self._open(self.base_url)

    def find_element(self, *loc):
        '''重写元素定位方法'''      
        try:
            # 确保元素是可见的。
            # 注意：入参本身是元组，不需要加*
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(loc))
            # WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(loc))
            # 对定位到的元素进行高亮
            # self.driver.execute_script("arguments[0].style.border='3px solid red'", element)
            # return element
        # except TimeoutException as errmsg:
            # self.log.error(f'定位{loc}超时：{errmsg}', exc_info=True)
        except Exception as allerr:
            self.log.exception(f'定位{loc}时发生异常：{allerr}')
        else:
            self.log.info(f'查找元素:{loc} 成功！')
        return self.driver.find_element(*loc)

    def switch_frame(self, *loc):
        '''重写switch_to_frame方法'''
        self.log.info(f'切换到ifram框架：{loc}')
        return self.driver.switch_to_frame(*loc)

    def script(self, src):
        '''定义script方法，用于执行js脚本，范围执行结果'''
        self.log.info(f'执行js脚本：{src}')
        self.driver.execute_script(src)
