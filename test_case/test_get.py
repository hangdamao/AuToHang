# author = "hang"
# created 14.08.2019

from base.requests_base import RequestsBase
from base.log_base import MyLog
from tool.format_test_data import format_data
from base.config_base import ConfigBase
import pytest

logger = MyLog("test_get")


class TestGet:

	case_file = "\\configs\\get_cases.yaml"
	api_rely_file = "\\configs\\api_post_rely_get.yaml"
	params_list = format_data(case_file)

	@pytest.mark.parametrize("case_name, run_method, api_path, time_out, headers, params", params_list)
	def test_get(self, case_name, run_method, api_path, time_out, headers, params):
		@RequestsBase(case_name=case_name,
					  run_mothed=run_method,
		              api_path=api_path,
		              time_out=time_out,
		              headers=headers,
		              params=params
		              )
		def inner_get():
			logger.info(f"用例：{case_name}, 测试完毕。")
		result = inner_get()
		assert isinstance(result, dict)

	def test_get_general(self):
		case_name = "test_get_general"
		api_path = "/get"
		@RequestsBase(case_name=case_name,
		              run_mothed="get",
		              api_path=api_path,
		              time_out=3,
		              headers=None,
		              params={"a": "0000000000000000000000111111111111",
		                      "b": "=====================1111111111111=========="}
		              )
		def inner_get():
			logger.info(f"用例：{case_name}, 测试完毕。")
		result = inner_get()
		assert result.get("args").get("a") == "0000000000000000000000111111111111"
		with ConfigBase(self.api_rely_file) as c_b:
			c_b.operation_yaml('w', result)
			logger.info(f"{api_path}接口依赖数据已准备完毕。")


if __name__ == '__main__':
	pytest.main(['-s', 'test_get.py'])