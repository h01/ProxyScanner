#-*- coding:utf-8 -*-
'''
	@name	GenIPS
	@modify	2014/11/27
	@author	Holger
	@github	https://github.com/h01/ProxyScanner
	@myblog	http://ursb.org
'''
class genips:
	def i2n(self, i):
		''' ip to number '''
		ip = [int(x) for x in i.split('.')]
		return ip[0] << 24 | ip[1] << 16 | ip[2] << 8 | ip[3]

	def n2i(self, n):
		''' number to ip '''
		return '%s.%s.%s.%s'%(
			(n & 0xff000000) >> 24,
			(n & 0x00ff0000) >> 16,
			(n & 0x0000ff00) >> 8,
			 n & 0x000000ff
		)

	def gen(self, s, e):
		''' genIPS:s=startIP(192.168.1.1);e=endIP(192.168.1.255) '''
		return [self.n2i(n) for n in range(self.i2n(s), self.i2n(e) + 1) if n & 0xff]