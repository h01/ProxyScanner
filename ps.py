#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
	@name	ProxyScanner
	@modify	2014/11/27
	@author	Holger
	@github	https://github.com/h01/ProxyScanner
	@myblog	http://ursb.org
'''
from libs.base import base
import getopt, sys

if __name__ == '__main__':
	base = base()
	try:
		opts, args = getopt.getopt(sys.argv[1:], 'vhi:p:t:s:', ['version', 'help', 'ips=', 'port=', 'thread=', 'save='])
		base.run(opts)
	except Exception,e:
		base.usage()