# -*- encoding: utf-8 -*-
'''
@Author  :   {Yixu}
@Contact :   {xiyu111@mail.ustc.edu.cn}
@Software:   PyCharm
@File    :   config_spider.py.py
@Time    :   2021/9/20 23:14
'''
# 用于读取config文件

import configparser
import logging

class ConfigArgs():
	"""
    用于加载spider.conf中的参数设置

     Attributes:
        file_path   :  存放配置的文件路径
        config_dict :  存放参数的字典
    """
	def __init__(self,conf_path):
		self.file_path = conf_path
		self.config_dict = {}

	def init(self):
		"""
		实际加载执行代码
		"""
		config = configparser.ConfigParser() #实例化conf加载类
		try:
			#print(self.file_path)
			conf_res = config.read(self.file_path)

		except configparser.MissingSectionHeaderError as e:
			logging.error(' * Config-file error: %s' % e)#若conf文件格式错误则报错
			return False
		except Exception as e:
			logging.error(' * Config-file error: %s' % e)#其他错误
			return False
		#print(self.file_path)
		#print(conf_res)
		if len(conf_res) == 0:
			logging.error(' * Config-file error: there is no args' )
			return False #格式正确，无参数，报错

		try: #section是spider，key是后一个数字
			self.config_dict['url_list_file'] = config.get('spider', 'url_list_file').strip()
			self.config_dict['output_directory'] = config.get('spider', 'output_directory').strip()
			self.config_dict['max_depth'] = config.getint('spider', 'max_depth')
			self.config_dict['crawl_timeout'] = config.getfloat('spider', 'crawl_timeout')
			self.config_dict['crawl_interval'] = config.getfloat('spider', 'crawl_interval')
			self.config_dict['target_url'] = config.get('spider', 'target_url').strip()
			self.config_dict['thread_count'] = config.getint('spider', 'thread_count')#7个config参数
			self.config_dict['try_times'] = 3 #默认重试三次
			self.config_dict['tag_dict'] = {'a':'href', 'img':'src', 'link':'href', 'script':'src'} #目标内容
		except configparser.NoSectionError as e:#里面没有Section spider
			logging.error(' * Config_File not exists error : No section: \'spider\', %s' % e)
			return False
		except configparser.NoOptionError as e:#里面参数不对
			logging.error(' * Config_File not exists error : No option, %s' % e)
			return False
		#print('----------------')
		return True

	def get_url_list_file(self):
		"""
		返回要爬的网址列表
		"""
		return self.config_dict['url_list_file']

	def get_output_dir(self):
		"""
		返回要输出的文件夹路径
		"""
		return self.config_dict['output_directory']

	def get_max_depth(self):
		"""
		返回最大深度
		"""
		return self.config_dict['max_depth']

	def get_crawl_timeout(self):
		"""
		返回爬取超时时间
		"""
		return self.config_dict['crawl_timeout']

	def get_crawl_interval(self):
		"""
		返回爬取间隔时间
		"""
		return self.config_dict['crawl_interval']

	def get_target_url(self):
		"""
		返回目标url
		"""
		return self.config_dict['target_url']

	def get_thread_count(self):
		"""
		返回线程数目
		"""
		return self.config_dict['thread_count']

	def get_try_times(self):
		"""
		返回爬取最大尝试次数
		"""
		return self.config_dict['try_times']

	def get_tag_dict(self):
		"""
		返回目标内容种类词典
		"""
		return self.config_dict['tag_dict']

if __name__ == "__main__":
	A = ConfigArgs("spider.conf")
	A.init()


