# -*- encoding: utf-8 -*-
'''
@Author  :   {Yixu}
@Contact :   {xiyu111@mail.ustc.edu.cn}
@Software:   PyCharm
@File    :   test_html_par.py
@Time    :   2021/9/21 19:38
'''
import unittest
import sys
import os

sys.path.append('../')

import html_par

class Test_Html_Parse(unittest.TestCase):
	"""
	对 htmlParse.htmlParse类进行测试
	"""
	def setUp(self):
		content = """
            img{-ms-interpolation-mode:bicubic}
        """
		ddict = {'a':'href', 'img':'src', 'link':'href', 'script':'src'}
		self.htmlparser = html_par.HTML_class(content, ddict, 'www.baidu.com')

	def test_find_url(self):
		"""
		测试 extract_url function
		"""
		url_example = b'http://www.baidu.com/'
		self.assertIn(url_example, self.htmlparser.find_url())

	def test_unicode_to_utf8(self):
		"""
		测试Func - enc_to_utf8() of unicode_
		"""
		self.htmlparser.content = '百度人摆渡魂，百度都是人上人'
		self.assertTrue(self.htmlparser.enc_to_utf8())

	def test_gbk_to_uft8(self):
		"""
		测试 gkb转utf8
		"""
		self.htmlparser.content =  '百度人摆渡魂，百度都是人上人'.encode('gbk')
		self.assertTrue(self.htmlparser.enc_to_utf8())

	def test_utf8_utf8(self):
		"""
		测试utf8编码函数
		"""
		self.htmlparser.content = '百度人摆渡魂，百度都是人上人'.encode('utf-8')
		self.assertTrue(self.htmlparser.enc_to_utf8())

	def tearDown(self):
		self.htmlparser = None

if __name__ == '__main__':
	unittest.main()





