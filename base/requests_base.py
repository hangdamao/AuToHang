# author ="demo"
# created 05.07.2019

import json
import requests
from base import log_base
from base.exception_base import BaseException
from base.config_base import ConfigBase

logger = log_base.MyLog("requests_base")
with ConfigBase("\\configs\\config.ini") as c_b:
	config = c_b.read_ini()
	my_host = config['host']['my_host']


class RequestsBase(object):

	logger.info("测试开始，服务器连接中...")

	def __init__(self, **items):
		self.__host = my_host
		self.__run_mothed = items.get("run_mothed")
		self.__api_path = items.get("api_path")
		self.__time_out = items.get("time_out")
		self.__files = items.get("files")
		self.__case_name = items.get("case_name")
		with BaseException():
			if "params" in items.keys():
				self.__params = items.get("params")
			if "params" not in items.keys():
				self.__params = None
			if "headers" in items.keys():
				self.__headers = items.get("headers")
			if "headers" not in items.keys():
				self.__headers = {"Content-Type": "application/json"}

	def get_requests(self):
		with BaseException():
			with requests.Session() as session:
				response = session.get(url=self.__host + self.__api_path,
				                       params=self.__params,
				                       headers=self.__headers,
				                       timeout=float(self.__time_out),
				                       )
				if response.status_code == 200:
					return eval(response.content)
				return response

	def post_requests(self):
		with BaseException():
			with requests.Session() as session:
				if self.__headers.get("Content-Type") == "application/json":
					response = session.post(url=self.__host + self.__api_path,
					                        json=self.__params,
					                        headers=self.__headers,
					                        files=self.__files,
					                        timeout=float(self.__time_out),
					                        )
					if response.status_code == 200:
						return eval(response.content)
					return response
				if self.__headers.get("Content-Type") == "application/x-www-form-urlencoded":
					response = session.post(url=self.__host + self.__api_path,
					                        data=self.__params,
					                        headers=self.__headers,
					                        files=self.__files,
					                        timeout=float(self.__time_out),
					                        )
					if response.status_code == 200:
						return eval(response.content)
					return response

	def __call__(self, func, *args, **kwargs):
		if self.__run_mothed == "get":
			res = self.get_requests()
		if self.__run_mothed == "post":
			res = self.post_requests()
		def wrapper(*args, **kwargs):
			if isinstance(res, dict):
				out_res = json.dumps(res, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ':'))
				logger.info(f"【用例：{self.__case_name}， 接口：'{self.__host + self.__api_path}'】-- 测试结果如下：\n{out_res}")
				func(*args, **kwargs)
				return res
			else:
				logger.error(f"接口请求异常: {res.status_code}")
		return wrapper


def test_1():
	@RequestsBase(run_mothed ="get", api_path ="/get", time_out =3, case_name="get_case_01")
	def inner_get():
		logger.info("用例：get_case_01, 测试完毕。")
	res = inner_get()
	assert res is not None

def test_2():
	@RequestsBase(run_mothed ="post",
	              api_path = "/post",
	              time_out = 3,
	              params={"导演/演员/时间/...":"导演: 彼得·杰克逊 Peter Jackson   主演: 伊利亚·伍德 Elijah Wood / 西恩... / 美国 新西兰 / 剧情 动作 奇幻 冒险",
						    "影评":"9.0 328420人评价",
						    "电影名称":"指环王2：双塔奇兵",
						    "电影封面":"https://img3.doubanio.com/view/photo/s_ratio_poster/public/p909265336.jpg",
						    "电影总结":"承前启后的史诗篇章",
						    "电影详情页":"https://movie.douban.com/subject/1291572/"},
	              case_name="post_case_01")
	def inner_post():
		logger.info("用例：post_case_01, 测试完毕。")
	res = inner_post()
	assert res is not None


if __name__ == '__main__':
	test_1()
	test_2()
