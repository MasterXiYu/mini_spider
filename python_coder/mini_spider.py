# -*- encoding: utf-8 -*-
'''
@Author  :   {Yixu}
@Contact :   {xiyu111@mail.ustc.edu.cn}
@Software:   PyCharm
@File    :   mini_spider.py
@Time    :   2021/9/20 22:23
'''
import queue
import threading
import config_spider
import logging
import codecs
import re
import os
import crawl_spider
import url_object


class MiniSpider():
	"""
	程序执行

	Attributes:
		check_url_queue   : 待爬URL的队列
		checked_url       : 存放已经爬取过URL的队列
		config_file_path  : 配置文件路径
		error_url         : 存放访问出错URL的队列
		lock              : 线程锁
	"""

	def __init__(self, config_file_path='./spider.conf'):
		"""
		Initialize variables
		"""
		self.checking_url = queue.Queue(0) #0表示队列无上限
		self.checked_url = set() #set用于去重
		self.error_url = set()
		self.config_file_path = config_file_path #config路径
		self.lock = threading.Lock() #线程锁

	def init(self):
		"""
		Initialize ConfigArgs parameters

		Returns:
			True / False : 相关配置文件正常返回True，否则返回False
		"""
		config_arg = config_spider.ConfigArgs(self.config_file_path)
		is_load = config_arg.init()
		#is_load = False
		if not is_load:
			self.end('there is no conf file !')
			return False

		self.url_list_file = config_arg.get_url_list_file()#加载要爬取网站
		self.output_dir = config_arg.get_output_dir()#加载输出文件夹
		self.max_depth = config_arg.get_max_depth()#加载最大抓取深度
		self.crawl_interval = config_arg.get_crawl_interval()#加载爬取间隔时间
		self.crawl_timeout = config_arg.get_crawl_timeout()#加载失败最大时间
		self.target_url = config_arg.get_target_url()#加载目标网址
		self.thread_count = config_arg.get_thread_count()#加载线程数
		self.tag_dict = config_arg.get_tag_dict()#加载目标类型
		self.url_pattern = re.compile(self.target_url)#字符串匹配
		seedfile_is_exist = self.get_seed_url() #加载
		return seedfile_is_exist

	def end(self, info):
		"""
		退出程序的后续信息输出函数

		Args:
			info : 退出原因信息

		Returns:
			none
		"""
		logging.info('program is ended ... ')
		logging.info('reason of ending :' + info)
		logging.info('crawled  pages  num : {}'.format(len(self.checked_url)))
		logging.info('error page num : {}'.format(len(self.error_url)))

	def get_seed_url(self):
		"""
		加载目标网址的种子文件，若无则返回False

		:return:
			True/false:存在为True，否则为False
		"""
		#print(self.url_list_file)
		if not os.path.isfile(self.url_list_file):
			logging.error(' * start_url file is not existing!')
			self.end('there is no start_url!')
			return False
		#print('----------------------')
		with codecs.open(self.url_list_file,'r',encoding='utf8') as readfile:
			for line in readfile:
				if line.strip() == '':
					continue
				#print('*************************')
				url_obj = url_object.Url(line.strip(), 0)#取url生成url_obj备用
				#print(url_obj)
				self.checking_url.put(url_obj)#存入待访问队列中

		return True

	def print_config(self):
		'''
		调试用，打印配置信息
		:return:None
		'''
		print('* MiniSpider Configurations list as follows:')
		print('* %-15s  %s' % ('url_list_file   :',self.url_list_file))
		print('* %-15s  %s' % ('output_directory:',self.output_dir))
		print('* %-15s  %s' % ('max_depth       :',self.max_depth))
		print('* %-15s  %s' % ('crawl_interval  :',self.crawl_interval))
		print('* %-15s  %s' % ('crawl_timeout   :',self.crawl_timeout))
		print('* %-15s  %s' % ('target_url      :',self.target_url))
		print('* %-15s  %s' % ('thread_count    :',self.thread_count))

	def threads(self):
		thread_dict = {}
		thread_dict['output_dir'] = self.output_dir
		thread_dict['crawl_interval'] = self.crawl_interval
		thread_dict['crawl_timeout'] = self.crawl_timeout
		thread_dict['url_pattern'] = self.url_pattern
		thread_dict['max_depth'] = self.max_depth
		thread_dict['tag_dict'] = self.tag_dict

		for i in range(self.thread_count):
			this_thread = 'theard - %d' % i
			thread = crawl_spider.theard(this_thread,
										 self.process_request,
										 self.process_response,
										 thread_dict)
			thread.setDaemon(True)# 主线程退出时，后端线程退出
			thread.start()
			print (("第%s个线程开始工作") % i)
			logging.info(("第%s个线程开始工作") % i)

		self.checking_url.join()
		self.end('normal exits ')


	def process_request(self):
		"""
		返回一个url-object变量

		Returns:
			url_obj : 取出的url-object 对象
		"""
		url_obj = self.checking_url.get()#从队列中返回一个对象，如队列为空则返回为空
		return url_obj

	def process_response(self, url_obj, flag, extract_url_list=None):
		"""
        返回内容处理函数：

        Args:
            extract_url_list : 返回抽取出的urls集合
            url_obj  : 被下载页面的url的对象
            flag     : 页面下载具体情况的返回标志
                     - 0  : 表示下载成功且为非pattern页面
                     - 1  : 表示下载成功且为符合pattern的图片
                     - -1 : 表示页面下载失败
                     - 2  : depth >= max_depth 的非target - URL
        """
		if self.lock.acquire():#获取到资源锁
			if flag == -1:
				self.error_url.add(url_obj)#错误日志已被打印，这边就不重复打印了

			elif flag == 0:
				self.checked_url.add(url_obj)
				for sub_url in extract_url_list:
					next_url_obj = url_object.Url(sub_url, int(url_obj.get_depth()) + 1)
					if not self.visited(next_url_obj):
						self.checking_url.put(next_url_obj)

			elif flag == 1:
				self.checked_url.add(url_obj)

			else:#为2时不进行任何处理
				pass

			self.checking_url.task_done()

		self.lock.release()

	def visited(self,url_obj):
		"""
		检查查询过的网址里面有没有现在在查的网址
		:return:True/False
		"""
		for checked_url in self.checked_url:
			if url_obj.get_url() == checked_url.get_url():
				return True

		for error_url in self.error_url:
			if url_obj.get_url() ==  error_url.get_url():
				return True

		return False







