from selenium import webdriver
import time
import xlrd

driver = webdriver.Chrome()
driver.implicitly_wait(3)

def open_csc(csc_url):
    '''通过指定的ip地址登录csc'''
    global driver    
    driver.get(csc_url)
    driver.set_window_size(1366,768)
    driver.find_element_by_id('username').send_keys('wjx')
    driver.find_element_by_id('password').send_keys('Admin123')
    driver.find_element_by_id('adUser').click()
    driver.find_element_by_name('submit').click()
    # 通过查找页面上是否有“首页”二字来判断是否登录成功
    if driver.find_element_by_link_text('首页'):
        print('登录成功')
    time.sleep(2)
    # 登录成功后跳转到产品定义页面
    driver.get(csc_url + '#pages/xycustom/services/product_definitions/index')

# 新增操作系统类型
def add_os_type(ostype):
    '''添加操作系统类型'''
    print('开始添加操作系统类型：', ostype)
    global driver
    driver.find_element_by_xpath('//*[@data-bind="click: addOsType"]').click()
    driver.find_element_by_xpath('//*[@placeholder="名称"]').send_keys(ostype)
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="add_submitOsType"]').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@data-dismiss="modal"]/span').click()
    

# 在已有的操作系统类型上添加版本
def add_os_version(os_type, os_version):
    '''在某个操作系统类型下添加具体的操作系统版本'''
    global driver
    time.sleep(1)
    driver.find_element_by_link_text(os_type).click()
    time.sleep(1)

    # 判断操作系统类型下面是否有操作系统版本
    try:
        os_version_list = driver.find_elements_by_xpath('//div[@id="page-content"]//td[@data-bind="text: name"]')
        for os in os_version_list:
            # 如果要增加的操作系统版本已经存在，则退出此次添加
            if os.text == os_version:
                print('操作系统版本已存在：', os_version)
                return None
    except:
        print('开始添加操作系统版本：', os_version)

    driver.find_element_by_link_text('添加版本').click()
    time.sleep(1)
    driver.find_element_by_xpath('//input[@placeholder="操作系统版本名称"]').send_keys(os_version)
    driver.find_element_by_xpath('//input[@placeholder="输入1-99"]').send_keys('1')
    driver.find_element_by_id('add_submitOsVersion').click()

    # 检查是否在其他操作系统类型下有同名的版本
    try:
        time.sleep(1)
        # driver.find_element_by_xpath('//*[@class="modal fade in"]//div[@class="modal-body"]')
        driver.find_element_by_xpath('//div[text()="该名称系统版本已经存在！"]')
        print("该版本在其他类型下有重名")
        driver.find_element_by_xpath('//button[@aria-label="Close"]').click()
        time.sleep(1)
        driver.find_element_by_xpath("//a[text()='取消']").click()
        return None
    except:
        print('添加操作系统版本成功：', os_version)

    driver.find_element_by_xpath('//button[@aria-label="Close"]').click()


def set_os(xls_file, sheet_id):
    '''根据excel文件中的内容来添加操作系统'''
    global driver

    data = xlrd.open_workbook(xls_file) # 打开xls文件
    table = data.sheets()[sheet_id] # 打开第n张表
    nrows = table.nrows # 获取表的行数
    for i in range(1, nrows):
        os_type = table.row_values(i)[0]
        os_version = table.row_values(i)[1]
        print('读取excel文件中的操作系统类型和版本：{}  {}'.format(os_type, os_version))
        # 如果操作系统类型存在，则直接添加操作系统版本，否则添加该操作系统类型
        try:
            driver.find_element_by_link_text(os_type)
            print('操作系统类型已存在：', os_type)
        except:
            add_os_type(os_type)
        add_os_version(os_type, os_version)


if __name__ == '__main__':
    open_csc('https://192.168.219.222:8099/csc/index.html')
    set_os('ostype.xls', 1)