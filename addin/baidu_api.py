from aip import AipOcr

""" 百度 APPID AK SK 数据来源：https://console.bce.baidu.com/ai/#/ai/ocr/app/list"""
APP_ID = '11592396'
API_KEY = '0lHD0K0gWrmEBanFbHQ30BdB'
SECRET_KEY = 'embCdDHEuQVaNWjtNkcO0xbcwoaR0hkU '
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

def get_file_content(filePath):
    """ 读取本地图片，并返回识别的文本"""
    options = {}
    options["language_type"] = "ENG"
    options["detect_direction"] = "true"
    options["detect_language"] = "true"
    options["probability"] = "true"
    with open(filePath, 'rb') as fp:
        result = client.basicGeneral(fp.read(), options)
        if result['words_result']:
            return result['words_result'][0]['words'].replace(' ','')
        else:
            return None

print(get_file_content('E:\\OneDrive\\MYpy\\winhong\\CSC7\\captcha.jpg'))
print(get_file_content('E:\\OneDrive\\MYpy\\winhong\\CSC7\\captcha2.jpg'))