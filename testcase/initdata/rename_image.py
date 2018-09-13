'''通过连查csc和wce 2个数据库的镜像信息，来更新csc上的镜像操作系统版本'''
import pymysql
import image2os

# 连接csc数据库
CSC_CONN = pymysql.connect(
    host='192.168.219.222',
    user='csc',
    passwd='csc',
    db='csc',
    port=3306,
    charset='utf8'
)
CSC_CUR = CSC_CONN.cursor()

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


def update_os_type(os_type, wce_id, csc_conn):
    '''通过传入的操作系统版本和底层id，更新csc上的镜像信息'''
    # print('传入：', os_type, len(os_type))
    op_type, op_version = image2os.find_image_os(os_type)
    try:
        csc_update_image = '''UPDATE csc_resource_image SET OP_TYPE_ = '{}', OP_VERSION_ = '{}' WHERE ORIGINAL_ID_ = "{}" '''.format(
            op_type, op_version, wce_id)
        print("\t执行：", csc_update_image)
        csc_update_cur = csc_conn.cursor()
        csc_update_cur.execute(csc_update_image)
        csc_conn.commit()
        print("\t更新成功！")
    except:
        csc_conn.rollback()
        csc_conn.close()


def find_os_type(wce_cur, wce_id):
    '''通过传入wce的游标和底层id，循环在xxx_vm_template 3个镜像表中查找操作系统版本'''
    vm_type_list = ['pvm', 'vmw', 'ws']
    for vm_type in vm_type_list:
        find_os = '''SELECT OS_VERSION from {}_vm_template where ORIGINAL_ID = "{}"'''.format(
            vm_type, wce_id)
        wce_cur.execute(find_os)
        result = wce_cur.fetchall()
        if result:
            return result[0][0]
    return None


# 查找csc镜像对应的底层uuid, 和现保存的操作系统版本
CSC_SELECT_IMAGE = '''SELECT ORIGINAL_ID_, OP_VERSION_ FROM csc_resource_image WHERE DISK_FORMAT_ IS NULL GROUP BY ORIGINAL_ID_'''
CSC_CUR.execute(CSC_SELECT_IMAGE)
IMAGE_DATA = CSC_CUR.fetchall()
if IMAGE_DATA:
    COUNTER = 1
    for data in IMAGE_DATA:
        print('')
        wce_id = data[0]
        print("查找到第{}条数据：".format(COUNTER))
        COUNTER = COUNTER + 1
        print('\t底层UUID为:', wce_id)
        os_type = find_os_type(WCE_CUR, wce_id)
        if os_type:
            print("\t查找到的操作系统版本为：", os_type)
            wce_type, wce_version = image2os.find_image_os(os_type)
            print("\t底层映射的操作系统版本为：", wce_version)
            csc_version = data[1]
            print("\tCSC上的操作系统版本为：", csc_version)
            if csc_version == wce_version:
                print('\t与底层一致，无需更新')
            else:
                update_os_type(os_type, wce_id, CSC_CONN)
        else:
            print("\t没有找到操作系统版本")
            continue
else:
    print('未查找到csc上的镜像数据，请进行收集操作')

# 关闭数据库连接
CSC_CONN.close()
WCE_CONN.close()
