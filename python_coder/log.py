# -*- encoding: utf-8 -*-
'''
@Author  :   {Yixu}
@Contact :   {xiyu111@mail.ustc.edu.cn}
@Software:   PyCharm
@File    :   log.py
@Time    :   2021/9/20 14:32
'''

import os
import logging
import logging.handlers

def init_log(log_path, level=logging.INFO, when="D", backup=7,
			 format="%(levelname)s:%(asctime)s:%(filename)s:%(lineno)d * %(thread)d %(message)s",
			 datefmt="%m-%d %H:%M:%S"):
	"""
	init_log - 初始化日志

	Args:
	:param log_path: - 日志文件文件夹;
						日志文件写入以下两个文件中.log, .log.wf
						若文件不存在则会被创建
	:param level:    - 高于这个层级的信息会显示：
						DEBUG < INFO < WARNING < ERROR < CRITICAL
						默认层级: logging.INFO
	:param when:     - 使用区分日志文件的时间间隔
					'S' : Second 秒
					'M' : Minutes 分
					'H' : Hours 时
					'D' : Days 天
					'W' : Week day 周
					默认为: D
	:param backup: 默认保留的日志文件数量，默认为7
	:param format: 日志格式
					默认日志格式:
					%(levelname)s: %(asctime)s: %(filename)s:%(lineno)d * %(thread)d %(message)s
					 INFO: 09-20 18:02:42: log.py:40 * 1998656876656 HELLO WORLD
	:param datefmt:时间戳
	:return: No return

	Raises:
		OSError: 无法创建日志文件夹
		IOError: 无法打开日志文件

	"""

	formatter = logging.Formatter(format, datefmt) # 输出格式设置，以及时间戳
	logger = logging.getLogger() # 生成一个log对象，默认的返回了根节点root的log
	logger.setLevel(level) # 设置日志输出等级

	dir = os.path.dirname(log_path) # 输入设置的路径
	if not os.path.isdir(dir):# 路径不存在会被创建
		os.makedirs(dir)

	handler = logging.handlers.TimedRotatingFileHandler(log_path + ".log",
														when=when,
														backupCount=backup)#
	#普通的handle，应用于log

	handler.setLevel(level) #默认运行用的，大于info的会被写入
	handler.setFormatter(formatter)
	logger.addHandler(handler)
	# print('test')

	handler = logging.handlers.TimedRotatingFileHandler(log_path + ".log.wf",
														when=when,
														backupCount=backup)
	#调试用的handle，应用于.log.wf，
	handler.setLevel(logging.WARNING) #大于warning的才会被写入
	handler.setFormatter(formatter)
	logger.addHandler(handler)




