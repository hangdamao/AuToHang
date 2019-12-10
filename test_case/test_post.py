# author = "hang"
# created 14.08.2019

from base.requests_base import RequestsBase
from base.log_base import MyLog
from tool.format_test_data import format_data, format_post_rely_get
import pytest

logger = MyLog("test_post")


class TestPost:

	case_file = "\\configs\\post_cases.yaml"
	params_list = format_data(case_file)

	@pytest.mark.parametrize("case_name, run_method, api_path, time_out, headers, params", params_list)
	def test_post(self, case_name, run_method, api_path, time_out, headers, params):
		@RequestsBase(case_name=case_name,
					  run_mothed=run_method,
		              api_path=api_path,
		              time_out=time_out,
		              headers=headers,
		              params=params
		              )
		def inner_post():
			logger.info(f"用例：{case_name}, 测试完毕。")
		result = inner_post()
		assert isinstance(result, dict)

	def test_post_general_reply_get(self):
		rely_on_get_file = "\\configs\\api_post_rely_get.yaml"
		rely_params = format_post_rely_get(rely_on_get_file)
		case_name = "test_post_general_reply_get"
		@RequestsBase(case_name=case_name,
		              run_mothed="post",
		              api_path="/post",
		              time_out=3,
		              headers={"Content-Type": "application/json"},
		              params=rely_params
		              )
		def inner_post():
			logger.info(f"用例：{case_name}, 测试完毕。")
		result = inner_post()
		assert isinstance(result, dict)
		assert result.get("json").get("a") == "0000000000000000000000111111111111"


if __name__ == '__main__':
	pytest.main(['-s', 'test_post.py'])