# -*- encoding: utf-8 -*-
'''
@Author  :   {Yixu}
@Contact :   {xiyu111@mail.ustc.edu.cn}
@Software:   PyCharm
@File    :   test_downloader.py
@Time    :   2021/9/21 19:38
'''

import unittest
import sys
import re

sys.path.append('../')
import crawl_spider
import mini_spider

class TestCrawlThread(unittest.TestCase):
	"""
	对 crawl_thread 进行测试
	"""

	def setUp(self):
		miniSpider = mini_spider.MiniSpider('../spider.conf')
		url_pattern = re.compile('.*.jpg')
		args_dict = {}
		args_dict['output_dir'] = './urls'
		args_dict['crawl_interval'] = 1
		args_dict['crawl_timeout'] = 1
		args_dict['url_pattern'] = url_pattern
		args_dict['max_depth'] = 1
		args_dict['tag_dict'] = {}
		self.crawlthread = crawl_spider.CrawlerThread('thread-0',
													  miniSpider.process_request(),
													  miniSpider.process_response(),
													  args_dict)

	def test_is_targeturl(self):
		"""
		测试
		:return:
		"""
		url = 'http://img.firefoxchina.cn/2016/07/4/201607010831530.jpg'
		self.assertTrue(self.crawlthread.is_target_url(url))

	def test_is_not_targeturl(self):
		"""
		测试save_target() function
		"""
		url = 'http://img.firefoxchina.cn/2016/07/4/201607010831530.jpg'
		self.assertTrue(self.crawlthread.save_target(url))

	def tearDown(self):
		self.crawlthread = None
		self.configargs = None

if __name__ == "__main__":
	unittest.main()


