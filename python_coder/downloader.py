# -*- encoding: utf-8 -*-
'''
@Author  :   {Yixu}
@Contact :   {xiyu111@mail.ustc.edu.cn}
@Software:   PyCharm
@File    :   downloader.py.py
@Time    :   2021/9/21 16:43
'''
#下载用

import logging
import urllib.request

class Downloader():
	def __init__(self,url_obj,timeout,try_time = 3):
		self.url_obj = url_obj
		self.timeout = timeout
		self.try_time = try_time

	def download(self):
		for time in range(self.try_time):
			try:
				response = urllib.request.urlopen(self.url_obj.get_url(), timeout=self.timeout)
				response.depth = self.url_obj.get_depth()
				return (response, 0)

			except Exception as e:
				if time == self.try_time - 1:#尝试到了最后一次
					error_info = \
						'* Downloading failed : %s - %s' % (self.url_obj.get_url(), e)
					logging.warning(error_info)

			logging.warning(' * Try for {}th times'.format(time + 1))
			if time == self.try_time - 1:
				return (None, -1)