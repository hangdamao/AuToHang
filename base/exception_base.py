# author = "hang"
# created 13.08.2019

from base import log_base
from base import config_base
from requests import RequestException

logger = log_base.MyLog("base_exception")

# 读取配置文件
def get_config_datas(error_name):
	with config_base.ConfigBase("\\configs\\error_codes.yaml") as config:
		res = config.operation_yaml("r")
		for i in list(res):
			if i.get(error_name) is not None:
				return i.get(error_name)


class ErrorReason(object):
	def __init__(self, code, message):
		self.code = code
		self.message = message


class BaseException(Exception):
	"""base exception class, derived Exception"""

	def __init__(self, err_code=None, massage=None):
		self.__massage = massage
		self.__err_code = err_code

	def to_json(self):
		return {
			"status_code": self.__err_code,
			"massage": self.__massage
		}

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		if exc_type == KeyError:
			logger.error(f'属性值错误: \n {exc_type}, {exc_val}, {exc_tb}')
		if exc_type == RequestException:
			logger.error(f"接口请求异常: \n {exc_type}, {exc_val}, {exc_tb}")
			return None
		if exc_type == FileNotFoundError:
			logger.error(f"文件不存在: \n {exc_type}, {exc_val}, {exc_tb}")
			return None
		if exc_type ==FileExistsError:
			logger.error(f"文件已存在: \n {exc_type}, {exc_val}, {exc_tb}")
			return None
		if self.__err_code:
			return self.to_json()
		return True


if __name__ == '__main__':
	code, massage = get_config_datas("PARAM_ERROR")
	with BaseException(code, massage) as b_e:
		result = b_e.to_json()
		print(result)

	code, massage = get_config_datas("NOT_10_BYTES")
	with BaseException(code, massage) as b_e:
		result = b_e.to_json()
		print(result)
