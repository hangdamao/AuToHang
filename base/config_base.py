# author = "hang"
# created 10.07.2019
# encoding：utf-8

import datetime
import os
import ruamel
import warnings
from ruamel import yaml
from configparser import ConfigParser
from base import log_base

logger = log_base.MyLog("config_base")


def project_dir():
	# get current project directory

	current_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
	return current_dir


class ConfigBase:

	"""used to read and write files"""

	def __init__(self, tgt_file=None):
		# ready file and current project directory

		self.__tgt_file = project_dir() + tgt_file

	def __enter__(self):
		# with statement context manager: __enter__()

		return self

	def read_ini(self):
		# to read the ini file, you can operation like a list

		config = ConfigParser()
		config.read(self.__tgt_file, encoding="utf-8")
		logger.info("ini文件读取成功")
		return config

	def operation_yaml(self, mode='r', *data):
		# to operation the yaml file

		if mode == "w":
			with open(self.__tgt_file, 'w', encoding='utf-8') as f:
				yaml.dump_all(data, f, Dumper=yaml.RoundTripDumper)
				logger.info("yaml文件写入成功。")
		if mode == "r":
			warnings.simplefilter('ignore', ruamel.yaml.error.UnsafeLoaderWarning)
			with open(self.__tgt_file, 'r', encoding='utf-8') as f:
				result = yaml.load_all(f.read())
				logger.info("yaml文件读取成功。")
				return result
				# for i in result:     # 多个if下不允许出现生成器。
				# 	yield i

	def operation_json(self, mode='r', data=None):
		# to operation the json file

		if mode == "r":
			with open(self.__tgt_file, 'r') as f:
				res = f.read().split('\n')
				logger.info("json文件读取成功。")
				for i in res:
					if i == '':
						res.remove(i)
				return res
		if mode == 'w':
			with open(self.__tgt_file, 'a+') as f:
				f.write(str(data))
				f.write('\n')
				logger.info("json文件写入成功。")

	def __exit__(self, exc_type, exc_val, exc_tb):
		# with statement context manager: __exit__()

		if exc_type == FileNotFoundError:
			logger.error("文件不存在，或数据尚未准备好了！")
			return False
		if exc_type == FileExistsError:
			logger.error("文件已存在！")
			return False
		if exc_type != None:
			logger.error(f"文件操作失败: \n {exc_type}, {exc_val}, {exc_tb}")
			return exc_val, exc_tb
		return True  # True表示不会抛出异常信息， False会抛出异常


if __name__ == '__main__':
	ini_file = "\\configs\\config.ini"
	json_file = "\\configs\\test.json"
	yml_file = "\\configs\\test.yaml"
	data = {
		'platformName': 'Android',
		'platformVersion': '7.0',
		'deviceName': 'A5RNW18316011440',
		'appPackage': 'com.tencent.mm',
		'appActivity': '.ui.LauncherUI',
		'automationName': 'Uiautomator2',
		'unicodeKeyboard': True,
		'resetKeyboard': True,
		'noReset': True,
		'chromeOptions': {'androidProcess': 'com.tencent.mm:tools'}}
	test_data1 = {
		"test_1_ip_api": {
			"url":
				"http://httpbin.org/ip",
			"assert": {
				"ResponseType": ["type", "dict"],
				"origin": ["type", "str"]
			},
			"method":
				"get",
			"params":
				"",
			"desc":
				"\u6d4b\u8bd5httpbin\u7684ip\u63a5\u53e3\u8fd4\u56de\u6b63\u5e38"
		}
	}
	test_data2 = {"name": "dashuaihang"}
	test_data3 = {
		'platformName': 'Android',
		'platformVersion': '7.0',
		'deviceName': 'A5RNW18316011440',
		'appPackage': 'com.tencent.mm',
		'appActivity': '.ui.LauncherUI',
		'automationName': 'Uiautomator2',
		'unicodeKeyboard': True,
		'resetKeyboard': True,
		'noReset': True,
		'chromeOptions': {'androidProcess': 'com.tencent.mm:tools'}
	}
	test_data4 = [1, 2, 3, 4, 5, 6]
	test_data5 = """天行健。君子以自强不息"""
	test_data6 = (1, 3, 4, 433, 53)
	test_data7 = {
		'str': 'Hello World!',
		'int': 110,
		'float': 3.141,
		'boolean': True,
		'time': datetime.datetime(2016, 9, 22, 3, 43, 30, 200000).strftime('%Y-%m-%d %H:%M:%S'),
		'date': datetime.date(2016, 9, 22).strftime('%Y-%m-%d')
	}

	'''ini文件读取'''
	with ConfigBase(tgt_file=ini_file) as c_f:
		config = c_f.read_ini()
		logger.info(config['log_path']['my_log_path'])
		logger.info(config['host']['my_host'])

	'''json文件的读取与写入'''
	# with ConfigBase(tgt_file=json_file) as c_f:
		# 写入
		# c_f.operation_json(mode='w', data=data)
		# 读取
		# res = c_f.operation_json(mode='r')
		# logger.info(res)
		# logger.info(type(res))
		# logger.info(len(res))
		# logger.info(type(res[0]))
		# logger.info(type(eval(res[0])))

	'''yaml文件的读取和写入'''
	# with ConfigBase(tgt_file=yml_file) as c_b:
	# 	# 写入
	# 	c_b.operation_yaml('w', data, test_data1, test_data2, test_data3, test_data4, test_data5, test_data6, test_data7)
		# 读取
		# res = c_b.operation_yaml(mode='r')
		# logger.info(res)
		# ll = list(res)
		# logger.info(ll)
		# logger.info(len(ll))
	# for i in ll:
	# 	logger.info(type(i))

