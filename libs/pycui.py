#-*- coding:utf-8 -*-
'''
	@name		Python console color-output ui (PycUI)
	@blog		https://ursb.org
	@github		https://github.com/h01/pycui
	@update		2014/10/29
	@author		Holger
	@version	1.0
'''
from os import name

class color:
	def __init__(self):
		if name == "nt":
			# Windows
			self.RED    = 0x04
			self.GREY   = 0x08
			self.BLUE   = 0x01
			self.CYAN   = 0x03
			self.BLACK  = 0x0
			self.GREEN  = 0x02
			self.WHITE  = 0x07
			self.PURPLE = 0x05
			self.YELLOW = 0x06
			from ctypes import windll
			def s(c, h = windll.kernel32.GetStdHandle(-11)):
				return windll.kernel32.SetConsoleTextAttribute(h, c)
			def p(m, c = self.BLACK, e = True):
				s(c | c | c)
				if e:
					print m
				else:
					print m,
				s(self.RED | self.GREEN | self.BLUE)
		else:
			# Other system(unix)
			self.RED    = '\033[31m'
			self.GREY   = '\033[38m'
			self.BLUE   = '\033[34m'
			self.CYAN   = '\033[36m'
			self.BLACK  = '\033[0m'
			self.GREEN  = '\033[32m'
			self.WHITE  = '\033[37m'
			self.PURPLE = '\033[35m'
			self.YELLOW = '\033[33m'
			def p(m, c = self.BLACK, e = True):
				if e:
					print "%s%s%s"%(c, m, self.BLACK)
				else:
					print "%s%s%s"%(c, m, self.BLACK),
		self.p = p

class pycui:
	def __init__(self):
		self.c = color()
	def warning(self, m):
		self.c.p("[-] %s"%m, self.c.PURPLE)
	def info(self, m):
		self.c.p("[i] %s"%m, self.c.YELLOW)
	def error(self, m):
		self.c.p("[!] %s"%m, self.c.RED)
	def success(self, m):
		self.c.p("[*] %s"%m, self.c.GREEN)
	# short-func
	def w(self, m):
		self.warning(m)
	def i(self, m):
		self.info(m)
	def e(self, m):
		self.error(m)
	def s(self, m):
		self.success(m)
