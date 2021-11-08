# -*- encoding: utf-8 -*-
'''
@Author  :   {Yixu}
@Contact :   {xiyu111@mail.ustc.edu.cn}
@Software:   PyCharm
@File    :   html_par.py
@Time    :   2021/9/21 18:25
'''
import logging
import urllib
import bs4
import chardet
from urllib.parse import urljoin

class HTML_class():
	"""
	从html中提取出网址链接以及下载的url

	"""
	def __init__(self, content, link_tag_dict, url):
		'''

		:param content: 返回的html源码
		:param link_tag_dict: 待解析标签
		:param url: 待解析的url
		'''
		self.link_tag_dict = link_tag_dict
		self.content = content
		self.url = url

	def find_url(self):
		"""
		提取出url给后续递归查询

		:return:返回出多个url的列表

		"""
		extract_url_list = []
		if not self.enc_to_utf8():#没有得到utf-8的编码，直接无法爬取
			return extract_url_list

		soup = bs4.BeautifulSoup(self.content, 'html5lib') #爬取内容

		for tag, attr in self.link_tag_dict.items():
			all_found_tags = soup.find_all(tag) #找到所有符合要求的内容
			for found_tag in all_found_tags: # 搜索
				if found_tag.has_attr(attr): # 如果有相应的元素
					extract_url = found_tag.get(attr).strip() #提取url

					if extract_url.startswith("javascript") or len(extract_url) > 256:#如果是js脚本或者长度过长则放弃;
						continue

					if not (extract_url.startswith('http:') or extract_url.startswith('https:')):
						extract_url = urljoin(self.url, extract_url)

					extract_url_list.append(extract_url)#添加url给结果

		return extract_url_list#返回



	def enc_to_utf8(self):
		"""
		将编码转换为utf-8

		:return: True/false
		"""
		encoding = self.detect_encoding()
		#print(encoding)
		try:
			#print(encoding)
			if encoding is None:
				return False

			elif encoding.lower() == 'unicode':

				self.content = self.content.encode('utf-8')
				return True

			elif encoding.lower() == 'utf-8':
				return True

			else:
				self.content = self.content.decode(encoding, 'ignore').encode('utf-8')
				return True
		except Exception as e:
			logging.warning(' * EncodingError - %s - %s:' % (self.url, e))
			return False

	def detect_encoding(self):
		"""
		检测html文本编码

		Returns:
			encode_name / None :能检测出来返回编码名字，否则返回None
		"""
		try:
			encode_dict = chardet.detect(self.content)
			encode_name = encode_dict['encoding']
			return encode_name
		except Exception as e:
			logging.error(' * Error coding-detect: %s' % e)
			return None





