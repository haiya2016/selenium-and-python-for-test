'''数据库查找到的内容转换到Excel文件中，形成容易被程序处理的映射关系'''
import pymysql
import xlwt
import os,sys

realpath = os.path.abspath('..\\..') + '\\config'
sys.path.append(realpath)
print(sys.path)
from config import db_config

def sql2xls():
    # 连接wincenter数据库
    WCE_CONN = pymysql.connect(
        host='192.168.213.113',
        user='wincenter',
        passwd='wincenter',
        db='wce',
        port=3306,
        charset='utf8'
    )
    WCE_CUR = WCE_CONN.cursor()

    workbook = xlwt.Workbook()
    sheet1 = workbook.add_sheet('sheet1',cell_overwrite_ok=True)
    vm_type_list = ['pvm', 'vmw', 'ws']
    COUNTER = 0
    for vm_type in vm_type_list:
        find_os = '''SELECT OS_TYPE,OS_VERSION from {}_vm_template GROUP BY OS_VERSION'''.format(
            vm_type)
        WCE_CUR.execute(find_os)
        result = WCE_CUR.fetchall()
        for data in result:
            sheet1.write(COUNTER, 0, data[0])
            sheet1.write(COUNTER, 1, data[1])
            COUNTER = COUNTER + 1
    WCE_CONN.close()
    workbook.save('ostype1.xls')
