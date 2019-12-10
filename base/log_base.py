# created 05.08.2019
# author = "hang"

import os
import datetime
import logging
import time
from configparser import ConfigParser
from colorama import Fore, Style

config = ConfigParser()
current_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
config.read(f"{current_dir}\\configs\\config.ini", encoding="utf-8")


class MyLog(object):

	def __init__(self, logger):
		"""
        指定保存日志的文件路径，日志级别，以及调用文件
        将日志存入到指定的文件中
        :param logger:  定义对应的程序模块名name，默认为root
        """

		# 创建一个logger
		self.logger = logging.getLogger(name=logger)
		self.logger.setLevel(logging.DEBUG)  # 指定最低的日志级别 critical > error > warning > info > debug
		self.log_time = time.strftime("%Y-%m-%d", time.localtime())
		self.log_name = current_dir + f"{config['log_path']['my_log_path']}\\system-run-{self.log_time}.log"
		fh = logging.FileHandler(self.log_name, 'a')  # 追加模式  这个是python2的
		# fh = logging.FileHandler(self.log_name, 'a', encoding='utf-8')  # 这个是python3的
		fh.setLevel(logging.INFO)
		# 再创建一个handler，用于输出到控制台
		ch = logging.StreamHandler()
		ch.setLevel(logging.INFO)
		# 定义handler的输出格式
		formatter = logging.Formatter('%(message)s')
		# '[%(levelname)s] [%(filename)s->%(funcName)s line:%(lineno)d] %(asctime)s  %(message)s'
		fh.setFormatter(formatter)
		ch.setFormatter(formatter)
		# 给logger添加handler
		self.logger.addHandler(fh)
		self.logger.addHandler(ch)
		#  添加下面一句，在记录日志之后移除句柄
		# self.logger.removeHandler(ch)
		# self.logger.removeHandler(fh)
		# 关闭打开的文件
		fh.close()
		ch.close()

	def debug(self, msg):
		"""
        定义输出的颜色debug--white，info--green，warning/error/critical--red
        :param msg: 输出的log文字
        :return:
        """
		self.logger.debug(Fore.WHITE + f"[DEBUG] {self.get_now_time()} - " + str(msg) + Style.RESET_ALL)

	def info(self, msg):
		self.logger.info(Fore.GREEN + f"[INFO] {self.get_now_time()} - " + str(msg).replace(u'\xa0', u' ') + Style.RESET_ALL)

	def warning(self, msg):
		self.logger.warning(Fore.RED + f"[WARNING] {self.get_now_time()} - " + str(msg) + Style.RESET_ALL)

	def error(self, msg):
		self.logger.error(Fore.RED + f"[ERROR] {self.get_now_time()} - " + str(msg) + Style.RESET_ALL)

	def critical(self, msg):
		self.logger.critical(Fore.RED + f"[CRITICAL] {self.get_now_time()} - " + str(msg) + Style.RESET_ALL)

	@staticmethod
	def get_now_time():
		return datetime.datetime.now()


if __name__ == '__main__':
	log = MyLog(logger="test")
	log.debug("debug")
	log.info("info")
	log.error("error")
	log.warning("warning")
	log.critical("critical")
