# -*- encoding: utf-8 -*-
'''
@Author  :   {Yixu}
@Contact :   {xiyu111@mail.ustc.edu.cn}
@Software:   PyCharm
@File    :   test_crawl_spider.py
@Time    :   2021/9/21 19:39
'''
import unittest
import sys

sys.path.append('../')
import config_spider

class TestConfigArgs(unittest.TestCase):
	"""
	测试config_spider.py 是否能正确加载参数，重点是init函数
	"""

	def setUp(self):
		self.config_args = config_spider.ConfigArgs('../spider.conf')

	def test_load_from_file_success(self):
		"""
		测试导入数据函数 load_from_file()
		"""
		#print('1111111111111111111111111')
		#print(self.config_args.file_path)
		self.assertTrue(self.config_args.init())

	def test_load_from_file_fail(self):
		#print('2222222222222222222222222')
		#print(self.config_args.file_path)
		self.config_args.file_path = 'spider.conf' #设置一个错误的路径使得导入失败
		self.assertFalse(self.config_args.init())

	def tearDown(self):
		self.config_args = None

if __name__ == '__main__':
	unittest.main()

