# author = "hang"
# created 14..8.2019

from base.config_base import project_dir, ConfigBase
from base.log_base import MyLog
from tool.mail_base import SendMail
import os
import time

logger = MyLog("main")


# about test path
with ConfigBase(tgt_file="\\configs\\config.ini") as c_f:
	config = c_f.read_ini()
	test_case_path = project_dir() + config['test_case_path']['my_test_cases']
	test_report_path = project_dir() + config['report_path']['my_report_path']
	smtp_server = config['mail_config']['smtp_server']
	smtp_port = config['mail_config']['smtp_port']
	smtp_sender = config['mail_config']['smtp_sender']
	smtp_senderpassword = config['mail_config']['smtp_senderpassword']
	smtp_receiver = config['mail_config']['smtp_receiver']
	smtp_subject = config['mail_config']['smtp_subject']
	smtp_body = config['mail_config']['smtp_body']


def send_test_mail():
	# send test mail

	with SendMail(smtp_server= smtp_server,
                 smtp_port= smtp_port,
                 smtp_sender= smtp_sender,
                 smtp_senderpassword= smtp_senderpassword,
                 smtp_receiver= smtp_receiver,# ,"czk176@zcsmart.com"
                 smtp_subject= smtp_subject,
                 smtp_body= smtp_body) as sender:
		sender.send_mail()


def run_pytest_with_pytesthtml():
	# generate test report with pytest-html

	now =time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time()))
	logger.info(f"当前时间为：{now}")
	# os.system(f"pytest -v -s {test_case_path} --html={test_report_path}\\{now}.html") # 打印测试内容
	os.system(f"python3 -m pytest -v {test_case_path} --html={test_report_path}\\{now}.html") # 不打印测试内容
	# os.system(f'C:\\softuser\\FireFox\\firefox.exe {test_report_path}\\{now}.html')
	# send_test_mail()  # 发送测试邮件


if __name__ == '__main__':
	run_pytest_with_pytesthtml()