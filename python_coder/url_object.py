# -*- encoding: utf-8 -*-
'''
@Author  :   {Yixu}
@Contact :   {xiyu111@mail.ustc.edu.cn}
@Software:   PyCharm
@File    :   url_object.py
@Time    :   2021/11/08 19:24
'''

class Url(object):
	"""
	标记每一个url的路径和深度
	Attributes:
		url   : 字符串
		depth : url的深度
	"""

	def __init__(self, url, depth=0):
		self.__url = url
		self.__depth = depth

	def get_url(self):
		"""
		get Url-object's url
		"""
		return self.__url

	def get_depth(self):
		"""
		get Url-object's depth
		"""
		return self.__depth
