# -*- encoding: utf-8 -*-
'''
@Author  :   {Yixu}
@Contact :   {xiyu111@mail.ustc.edu.cn}
@Software:   PyCharm
@File    :   test_minispider.py
@Time    :   2021/9/21 19:38
'''
import unittest
import sys
import os

sys.path.append('../')
import mini_spider
import url_object

class Test_MiniSpider(unittest.TestCase):
	"""
	对miniSpider进行单元测试
	"""
	def setUp(self):
		self.miniSpider = mini_spider.MiniSpider('spider.conf')

	def test_initialize(self):
		"""
		测试是否能够成功初始化
		"""
		os.chdir('../')
		self.assertTrue(self.miniSpider.init())

	def test_not_visited(self):
		"""
		测试一个没有访问过的网址是否被访问
		"""
		url = url_object.Url("http://www.baidu.com")
		self.assertFalse(self.miniSpider.visited(url))

	def test_has_visited(self):
		"""
		测试访问过后visit是否返回正常
		"""
		url = url_object.Url("http://www.baidu.com")
		self.miniSpider.checked_url.add(url)
		self.assertTrue(self.miniSpider.visited(url))

	def test_has_visited_err(self):
		"""
		测试访问错误后visit函数是否返回正常
		"""
		url = url_object.Url("http://www.baidu.com")
		self.miniSpider.error_url.add(url)
		self.assertTrue(self.miniSpider.visited(url))

	def test_over(self):
		"""
		釋放內存
		"""
		self.miniSpider = None

if __name__ == "__main__":
	unittest.main()



