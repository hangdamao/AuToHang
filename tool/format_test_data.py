# author = "hang"
# created 14.08.2019

from base.config_base import ConfigBase
from collections import deque
from base.log_base import MyLog
from base.exception_base import BaseException
import os

logger = MyLog("format_test_data")


def format_data(test_case_file):
	"""
	这里你可以从配置文件读取，也可以从数据库读取，还可以自己创造测试数据
	:param test_case_file:
	:return:
	"""
	params_list = []
	with ConfigBase(test_case_file) as config:
		res = config.operation_yaml('r')
		for i in list(res):
			if i is not None:
				inner_list = deque(eval(str(list(i.values()))[1:-1]).values())
				inner_list.appendleft(list(i.keys())[0])
				params_list.append(inner_list)
	return params_list


def format_post_rely_get(post_rely_get_file):
	"""
	解决数据post接口依赖数据问题
	:param post_rely_get_file:
	:return:
	"""
	with ConfigBase(post_rely_get_file) as c_b:
		res = list(c_b.operation_yaml('r'))
		if res is not None:
			for i in res:
				data = i.get("args")  # 被依赖字段
				return data


if __name__ == '__main__':
	format_post_rely_get("\\configs\\post_rely_get.yaml")
