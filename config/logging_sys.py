'''
日志系统，用于将日志输出到控制台和日志文件
'''
import logging
import logging.handlers

class Logger(object):
    '''日志系统'''
    def __init__(self, logger):
        '''
           指定保存日志的文件路径，日志级别，以及调用文件
           将日志存入到指定的文件中
        '''
        # 创建一个logger
        self.logger = logging.getLogger(logger)

        if not self.logger.handlers:        # 保证只有一个handles，避免重复输出日志
            self.logger.setLevel(logging.DEBUG)

            # 创建一个handler，用于写入日志文件
            file_handler = logging.FileHandler('.\\report\\test.log', encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)

            # 再创建一个handler，用于输出到控制台
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)

            # 定义handler的输出格式
            formatter = logging.Formatter('%(asctime)s - [%(levelname)s] - %(name)s - %(funcName)s - %(message)s')
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)

            # 给logger添加handler
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)

    def getlog(self):
        '''返回一个logger'''
        return self.logger

# datacenter_loc = (By.XPATH, '//*[@id="dragDiv5"]/div[2]/div[1]/select')
# lo = Logger('teset').getlog()
# lo.info(f'就是这样：{datacenter_loc}')
