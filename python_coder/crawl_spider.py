# -*- encoding: utf-8 -*-
'''
@Author  :   {Yixu}
@Contact :   {xiyu111@mail.ustc.edu.cn}
@Software:   PyCharm
@File    :   crawl_spider.py.py
@Time    :   2021/9/21 14:26
'''
#抓取源代码主要工具

import threading
import logging
import time
import os
import urllib.request
import downloader
import html_par
import urllib.parse


class theard(threading.Thread): #继承python的多线程
	"""
	线程话爬取代码，第一次会将网址爬取，然后翻入已爬取的set里面，直到爬取完毕
	"""

	def __init__(self,name_str,process_request,process_response,args_dict):
		super(theard,self).__init__(name = name_str) #多重继承
		self.process_request = process_request
		self.process_response = process_response
		self.output_dir = args_dict['output_dir']
		self.crawl_interval = args_dict['crawl_interval']
		self.crawl_timeout = args_dict['crawl_timeout']
		self.url_pattern = args_dict['url_pattern']
		self.max_depth = args_dict['max_depth']
		self.tag_dict = args_dict['tag_dict']

	def run(self):
		"""
		线程抓取目标并存储
		:return:
		"""
		while 1:
			url_obj = self.process_request() # 得到一个网址对象
			time.sleep(self.crawl_interval) # 防止被抓包的时间限制

			#.info('%-12s  : get a url in depth ' %
			#			 threading.currentThread().getName()) #打印抓取日志
			#print('----------------')
			#print(url_obj.get_url())
			#if url_obj.get_url() == None:
				#print('this is none')
			#print('----------------')
			if self.is_target_url(url_obj.get_url()):
				flag = -1
				if self.save_target(url_obj.get_url()):
					flag = 1 #成功保存目标
				self.process_response(url_obj, flag)
				continue

			if url_obj.get_depth() < self.max_depth:#可以爬取
				downloader_obj = downloader.Downloader(url_obj, self.crawl_timeout)
				response, flag = downloader_obj.download() #flag = 0 or -1

				if flag == -1: # download failed
					self.process_response(url_obj, flag)
					continue

				if flag == 0: # download sucess
					content = response.read()
					url = url_obj.get_url()
					soup = html_par.HTML_class(content, self.tag_dict, url)
					extract_url_list = soup.find_url()

					self.process_response(url_obj, flag, extract_url_list)
			else:
				flag = 2  # depth > max_depth 的正常URL
				self.process_response(url_obj, flag)



	def is_target_url(self,url):
		"""
		判断是否是图片的url
		:return:
			True/False : 若为图片则返回True 否则返回False
		"""
		found_aim =self.url_pattern.match(url) #.*.(gif|png|jpg|bmp)$ 只下载图片元素
		if found_aim:
			return True
		return False

	def save_target(self,url):
		'''
		将符合的图片保存在目标文件夹中
		:param url:
		:return:
		'''
		if not os.path.isdir(self.output_dir):
			os.mkdir(self.output_dir)

		file_name = urllib.parse.quote_plus(url) #编码

		if len(file_name) >64:
			file_name = file_name[-64:] #储存文件名

		target_path = "{}/{}".format(self.output_dir, file_name)
		try:
			urllib.request.urlretrieve(url, target_path) #直接调用包下载目标文件
			return True

		except IOError as e:
			logging.warning(' * Save picture Failed: %s - %s' % (url, e))#下载保存失败
			return False






