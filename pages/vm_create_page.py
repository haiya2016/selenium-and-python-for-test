# coding=utf-8
'''
Created on 2018-9-9
@author: wjx
Project:云主机创建页面
'''
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage
import time


class VmCreatePage(BasePage):
    '''
    继承BasePage类
    '''
    # 按钮
    return_button1_loc = (By.XPATH, "//div[1]/a/button")                        # 顶部返回按钮
    return_button2_loc = (By.XPATH, "//div[2]/a/button")                        # 底部返回按钮
    submit_button_loc = (By.XPATH, "//button[text()='立即执行']")                # 立即执行按钮
    confirm_button_loc = (By.XPATH, "//button[@data-bind='click: submit']")     # 提交确认按钮
    search_button_loc = (By.XPATH, "//*[text()='搜索']")                         # 搜索按钮
    reset_button_loc = (By.XPATH, "//*[text()='重置']")                          # 重置按钮
    first_search_result_loc = (By.XPATH, "//tbody/tr[2]//span")                  # 所有搜索的第一个结果
    
    # 基本信息
    name_input_loc = (By.XPATH, "//label[text()='云主机名称：']//..//input")
    vmname_input_loc = (By.XPATH, "//label[text()='VM Name：']//..//input")
    hostname_input_loc = (By.XPATH, "//form/div[2]/div[3]/div/div/input")
    service_loc = (By.XPATH, "//button[@data-bind='click: addService']")
    vdc_loc = (By.XPATH, "//button[@data-bind='click: addVdc']")
    user_loc = (By.XPATH, "//button[@data-bind='click: showUser']")
    bussys_loc = (By.XPATH, "//button[@data-bind='click: $root.addBusSys']")
    busitem_loc = (By.XPATH, "//button[@data-bind='click: $root.addBusItem']")
    applytime_forever_loc = (By.XPATH, "//*[@id='inlineRadio1']//..//span")
    applytime_time_loc = (By.XPATH, "//*[@id='inlineRadio2']//..//span")
    applytime_timefor_loc = (By.ID, '//*[@id="resource_instance_vm_limit_option2_unit"]')
    applytime_date_loc = (By.XPATH, "//*[@id='inlineRadio3']//..//span")
    applytime_datefor_loc = (By.ID, '//*[@id="resource_instance_vm_limit_option3"]')  
    textarea_input_loc = (By.XPATH, "//textarea")                               # 备注
    # 配置信息
    az_loc = (By.XPATH, "//label[text()='可用分区：']//..//select")
    image_loc = (By.XPATH, "//button[@data-bind='click:$root.addImage']")
    host_loc = (By.XPATH, "//button[@data-bind='click: $root.addHost']")
    storage_pool_loc = (By.XPATH, '//button[@data-bind="click:$root.addStoragePool"]')
    cpu_loc = (By.ID, 'resource_instance_cpu')
    memory_loc = (By.ID, 'resource_instance_memory')
    sysdisk_loc = (By.ID, "storage_input_id")
    ip_pool_loc = (By.ID, 'create_vm_ip_pool_id')
    # 服务选择页面
    service_search_input_loc = (By.XPATH, "//span[text()='服务名称']/../input")         # 服务搜索输入框
    service_confirm_loc = (By.XPATH, "//button[text()='确定']")                 # 确定按钮
    # VDC选择页面
    vdc_search_input_loc = (By.XPATH, "//span[text()='VDC名称']/../input")
    vdc_confirm_loc = (By.XPATH, "//button[text()='确认' and @data-bind='click: vdcSave']")
    # 归属用户选择页面
    user_search_input_loc = (By.XPATH, "//span[text()='账号']/../input")
    user_confirm_loc = (By.XPATH, "//button[text()='确认' and @data-bind='click: saveUsers']")
    # 业务系统选择页面
    bussys_search_input_loc = (By.XPATH, "//span[text()='业务系统名称']/../input")
    bussys_confirm_loc = (By.XPATH, "//button[text()='确认' and @data-bind='click: busSysSave']")
    # 应用集群选择页面
    busitem_search_input_loc = (By.XPATH, "//span[text()='应用集群名称']/../input")
    busitem_confirm_loc = (By.XPATH, "//button[text()='确认' and @data-bind='click: busItemSave']")

    # def open(self, url):
    #     '''定义open方法，调用_open()进行打开链接'''
    #     self._open(url, self.pagetitle)

    def search_for(self, item_type, item_value):
        '''根据item_type和item_value调用不同的组件进行搜索'''
        if item_type == '归属服务':
            self.find_element(*self.service_loc).click()
            time.sleep(2)
            print('查找到按钮')
            self.find_element(*self.service_search_input_loc).send_keys(item_value)
            # self.send_keys(self.service_search_input_loc, value=item_value)
            print('进入查询界面')
        elif item_type == '归属VDC':
            self.find_element(*self.vdc_loc).click()
            self.find_element(*self.vdc_search_input_loc).send_keys(item_value)
        elif item_type == '归属用户':
            self.find_element(*self.user_loc).click()
            self.find_element(*self.user_search_input_loc).send_keys(item_value)
        elif item_type == '业务系统':
            self.find_element(*self.bussys_loc).click()
            self.find_element(*self.bussys_search_input_loc).send_keys(item_value)
        elif item_type == '应用集群':
            self.find_element(*self.busitem_loc).click()
            self.find_element(self.busitem_search_input_loc).send_keys(item_value)
        print('查询结束：')
        self.find_element(*self.search_button_loc).click()           #  点击搜索按钮
        self.find_element(*self.first_search_result_loc).click()     # 勾选第一个搜索结果

    def item_click(self, item_type, item_value):
        '''搜索之后点击确认'''
        self.search_for(item_type, item_value)
        if item_type == '归属服务':
            self.find_element(*self.service_confirm_loc).click()
        elif item_type == 'VDC':
            self.find_element(*self.vdc_confirm_loc).click()
        elif item_type == '归属用户':
            self.find_element(*self.user_confirm_loc).click()
        elif item_type == '业务系统':
            self.find_element(*self.bussys_confirm_loc).click()
        elif item_type == '应用集群':
            self.find_element(*self.busitem_confirm_loc).click()

    def item_select(self, item_type, item_value):
        '''下拉列表的处理'''
        if item_type == '到期时间':
            select = Select(self.find_element(*self.applytime_timefor_loc))
        select.select_by_visible_text(item_value)

    def input_item(self, item_type, item_value):
        '''根据输入的类型和值进行填充'''
        if item_type == '云主机名称':
            self.find_element(*self.name_input_loc).send_keys(item_value)
        elif item_type == 'VMName':
            self.find_element(*self.vmname_input_loc).send_keys(item_value)
        elif item_type == 'Hostname':
            self.find_element(*self.hostname_input_loc).send_keys(item_value)
        elif item_type == '备注':
            self.find_element(*self.textarea_input_loc).send_keys(item_value)
        elif item_type == '到期时间':
            if item_value == '永久':
                self.find_element(*self.applytime_datefor_loc).click()
            elif '年' in item_value or '月' in item_value:
                self.find_element(*self.applytime_time_loc).click()
                self.item_select(item_type, item_value)
            else:
                self.find_element(*self.applytime_date_loc).click()
                self.find_element(*self.applytime_datefor_loc).send_keys(item_value)
        elif item_type == '归属服务':
            self.item_click(item_type, item_value)
        
                



    

