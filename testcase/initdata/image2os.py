import xlrd
# 读取xls文件
def find_image_os(image):
    image = image.rstrip()
    # print('要查找的值为：',image, len(image))
    # print(len(image))
    data = xlrd.open_workbook('ostype.xls') # 打开xls文件
    table = data.sheets()[0] # 打开第一张表
    nrows = table.nrows # 获取表的行数
    for i in range(nrows):
        # print(table.row_values(i)[2])
        if table.row_values(i)[2] == image:
            os = table.row_values(i)[0]
            os_version = table.row_values(i)[1]
            return os, os_version
    print(f'Excel表格中查找不到镜像对应的操作系统，请更新Excel表格对应关系：{image}')
    return None,None

# print(find_image_os('Microsoft Windows Server 2008 R2 Standard '))