# coding=utf-8
'''
Created on 2018-9-9
@author: wjx
Project:页面基本操作方法：如open，input_username，input_password，click_submit
'''
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage


class HomePage(BasePage):
    '''
    继承BasePage类
    '''
    datacenter_loc = (By.XPATH, '//*[@id="dragDiv5"]/div[2]/div[1]/select')
    dc_vm_loc = (By.XPATH, '//div[@class="resource-vm"]//strong')                           # 云主机
    dc_partition_loc = (By.XPATH, '//div[@class="resource-partition"]//strong')             # 可用分区
    dc_pool_loc = (By.XPATH, '//div[@class="resource-pool"]//strong')                       # 资源池
    dc_storageNum_loc = (By.XPATH, '//div[@class="resource-storageNum"]//strong')           # 存储池
    dc_image_loc = (By.XPATH, '//div[@class="resource-image"]//strong')                     # 镜像
    dc_host_loc = (By.XPATH, '//div[@class="resource-host"]//strong')                       # 宿主机
    dc_ip_loc = (By.XPATH, '//div[@class="resource-ip"]//strong')                           # IP池
    dc_network_loc = (By.XPATH, '//div[@class="resource-network"]//strong')                 # 网络
    dc_storageVolumen_loc = (By.XPATH, '//div[@class="resource-storageVolumen"]//strong')   # 存储
    dc_memory_loc = (By.XPATH, '//div[@class="resource-memory"]//strong')                   # 内存
    dc_cpu_loc = (By.XPATH, '//div[@class="resource-cpu"]//strong')                         # CPU
    resource_list = ['vm', 'partition', 'pool', 'host', 'storageNum', 'image', 'network', 'ip',
                     'storageVolumen', 'memory', 'cpu']


    def dc_select(self, dc_name):
        '''
        数据中心下拉列表选择，dc_name为数据中心的名称
        '''
        select = Select(self.find_element(*self.datacenter_loc))
        # print(select.all_selected_options)
        # print(select.all_selected_options.text)
        if dc_name in select.options.text:
            select.select_by_visible_text(dc_name)
        assert dc_name in select.options.text

    def db_check(self, csc_db, dc_name):
        '''检查数据中心的数据与数据库是否相符'''
        # csc_db = Database(**db_config)   # 连接数据库
        cursor = csc_db.cursor()
        sel_lists_dict = {
            'vm':f'''SELECT count(*) FROM csc_resource_instance_vm vm
                        LEFT JOIN csc_cloud_platform ccp ON vm.CLOUD_PLATFORM_UUID_ = ccp.UUID_
                        LEFT JOIN csc_data_center cdc ON ccp.DATACENTER_UUID_ = cdc.UUID_
                        WHERE cdc.NAME_ = '{dc_name}';''',
            'partition':f'''SELECT COUNT(*) FROM csc_az
                        LEFT JOIN csc_data_center cdc ON DATACENTER_UUID_ = cdc.UUID_
                        WHERE cdc.NAME_ = '{dc_name}';''',
            'pool': f'''SELECT count(*) from csc_resource_pool
                        LEFT JOIN csc_data_center cdc on DC_UUID_ = cdc.UUID_
                        WHERE cdc.NAME_ = '{dc_name}';''',
            'host': f'''SELECT count(*) from csc_host
                        LEFT JOIN csc_data_center cdc on DC_UUID_ = cdc.UUID_
                        WHERE cdc.NAME_ = '{dc_name}';''',
            # 'storageNum_sql':f'''''',
            'image':f'''SELECT count(*) from csc_resource_image
                        LEFT JOIN csc_az on AZ_UUID_ = csc_az.UUID_
                        LEFT JOIN csc_data_center cdc ON DATACENTER_UUID_ = cdc.UUID_
                        WHERE cdc.NAME_ = '{dc_name}';''',
            'network':f'''SELECT (if(CLOUD_PLATFORM_='CNware', 0, network_num_))
                        from csc_data_center WHERE	NAME_ = '{dc_name}';''',
            'ip':f'''SELECT (if(CLOUD_PLATFORM_!='CNware', 0, network_num_))
                        from csc_data_center WHERE	NAME_ = '{dc_name}';''',
            # 'storageVolumen':f'''''',
            # 'memory':f'''''',
            # 'cpu':f''''''
        }
        csc_count_dict = {}
        for key in sel_lists_dict:
            try:
                cursor.execute(sel_lists_dict[key]) 	# 执行sql语句
                results = cursor.fetchall()	            # 获取查询的所有记录
            except Exception as error:
                raise error
            csc_count_dict[key] = results[0][0]         # 将查询结果保存为字典
        return csc_count_dict

    def dc_check(self):
        '''以字典的形式返回页面上数据中心的数值'''
        resource_count_dict = {}
        for resource in self.resource_list:
            value = self.find_element(By.XPATH, f'//div[@class="resource-{resource}"]//strong').text
            resource_count_dict[resource] = value
        return resource_count_dict
