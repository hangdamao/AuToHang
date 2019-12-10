# author = "hang"
# created 10.07.2019

import pymysql.cursors
import log_base

logger = log_base.MyLog("data_base")


class DatabaseBase:
	"""connect DB mysql and access database"""

	def __init__(self, host, user, password, db, port, charset):
		self.__host = host
		self.__user = user
		self.__password = password
		self.__db = db
		self.__port = port
		self.__charset = charset

	def __enter__(self):
		self.connect = pymysql.Connect(
									host= self.__host,
									user= self.__user,
									password= self.__password,
									db= self.__db,
									port= self.__port,
									charset= self.__charset
								)
		if self.connect.server_status == 0:
			logger.info("数据库连接成功。")
			return self

	def access_sql(self, sql, how_many):
		self.cursor = self.connect.cursor()
		self.cursor.execute(sql)
		logger.info("sql执行结果如下：")
		if how_many == 'all':
			return self.cursor.fetchall()
		if how_many == 1:
			return self.cursor.fetchone()
		if how_many > 1:
			return self.cursor.fetchmany(how_many)

	def __exit__(self, exc_type, exc_val, exc_tb):
		if exc_type != None:
			logger.error(f"数据库操作出现异常：\n {exc_type}, {exc_val}, {exc_tb}")
		logger.info("数据操作完毕，即将关闭。")
		self.cursor.close()
		self.connect.close()
		return True


if __name__ == '__main__':
	sql = """SELECT pack_type from tsm_app_channel_pack WHERE business_id=6;"""
	how_many = "all"
	with DatabaseBase(host="172.18.91.14",
	                  user="tsm",
	                  password="tsm_mysql",
	                  db="zc_tsm",
	                  port=3306,
	                  charset="utf8") as d_b:
		res = d_b.access_sql(sql, how_many)
		logger.info(res)

