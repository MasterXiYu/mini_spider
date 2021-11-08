# -*- encoding: utf-8 -*-
'''
@Author  :   {Yixu}
@Contact :   {xiyu111@mail.ustc.edu.cn}
@Software:   PyCharm
@File    :   run_main.py.py
@Time    :   2021/9/20 14:24
'''

import argparse
import logging
import mini_spider

import log #导入日志模块



if __name__ == '__main__':
	'''
	主程序，程序入口
	'''
	log.init_log('./log_data/mini_spider')
	logging.info('%-35s' % ' * miniSpider is starting ... ')
	#logging.error('%-35s' % ' This is Error')
	# *********************************  start  ***********************
	# 这边是输出:
	# 命令行模式
	parser = argparse.ArgumentParser(description=None)
	parser.add_argument('-v',
						'--version',
						action='version',
						version='%(prog)s 1.0.0',
						help='显示版本信息') # 返回版本信息

	parser.add_argument('-c',
						'--config_file',
						action='store',
						dest='CONF_PATH',
						default='spider.conf',
						help='Set config file path')#设置conf文件，默认为spi.conf,dest为参数别名

	args = parser.parse_args()
	print("命令行设置完成，开始执行！")
	mini_spider = mini_spider.MiniSpider(args.CONF_PATH) #生成mini_spider类，并保存参数
	init = mini_spider.init()#初始化类别
	if init:
		mini_spider.print_config()#预处理输出
		mini_spider.threads()

	logging.info('%-35s' % ' * miniSpider is end ... ')
	print('完成搜索')






