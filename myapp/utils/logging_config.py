"""
time:241024
function:建立日志模块
auth:mayor
"""
import logging


class LoggingConfig:
    _instance = None
    logger = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(LoggingConfig, cls).__new__(cls, *args, **kwargs)
            cls._instance._configure_logger()
        return cls._instance
    #同时添加控制台日志和文件日志
    def _configure_logger(self):
        self.logger = logging.getLogger(__name__)
        if not self.logger.hasHandlers():
            # 设置日志级别
            self.logger.setLevel(logging.INFO)

            # 控制台处理器
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            console_handler.setFormatter(console_formatter)

            # 文件处理器
            file_handler = logging.FileHandler(r'C:\Users\jiany\myenv\Scripts\myproject\myapp\utils\server_logs.log')
            file_handler.setLevel(logging.INFO)
            file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(file_formatter)

            # 添加处理器到日志记录器
            self.logger.addHandler(console_handler)
            self.logger.addHandler(file_handler)

    def get_logger(self):
        return self.logger


if __name__ == '__main__':
    log = LoggingConfig()
    log.get_logger().info('hello,logging')