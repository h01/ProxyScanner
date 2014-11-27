#-*- coding:utf-8 -*-
'''
	@name	Base Functions
	@modify	2014/11/27
	@author	Holger
	@github	https://github.com/h01/ProxyScanner
	@myblog	http://ursb.org
'''
from pycui  import *
from genips import genips
import Queue, threading
import urllib2, socket

cui = pycui()
gen = genips()
cor = color()

class base:
	def __init__(self):
		self._p = 8080
		self._t = 10
		self._i = []
		self._o = []
		self._r = []
		self._s = ''
	def run(self, opts):
		for k, v in opts:
			if k in ['-v', '--version']:
				self.version()
			elif k in ['-p', '--port']:
				self._p = int(v)
			elif k in ['-i', '--ips']:
				_temp = v.split('-')
				self._i = gen.gen(_temp[0], _temp[1])
			elif k in ['-t', '--thread']:
				self._t = int(v)
			elif k in ['-s', '--save']:
				self._s = v
			else:
				self.usage()
		if (65535 >= self._p > 0) and (100 >= self._t > 0) and (len(self._i) > 0):
			self.start()
		else:
			self.usage()
	def start(self):
		cui.w('Proxy Scanner started')
		cui.i('Nums: %s'%len(self._i))
		cui.i('Port: %s'%self._p)
		cui.i('Thread: %s'%self._t)
		self.scanports()
		self.scanproxy()
		self.result()
	def scanports(self):
		cui.w('Start scanning the open port\'s IP..')
		def run(q):
			while not q.empty():
				_ip = q.get()
				if self.checkPort(_ip, self._p):
					cui.s('Open: %s'%_ip)
					self._o.append(_ip)
				else:
					cui.e('Close: %s'%_ip)
		self.startThread(self._i, run)

	def scanproxy(self):
		if len(self._o) > 0:
			cui.w('Checking the proxy is available..')
			def run(q):
				while not q.empty():
					_ip = q.get()
					if self.checkProxy(_ip, self._p):
						cui.s('OK: %s'%_ip)
						self._r.append(_ip)
					else:
						cui.e('NO: %s'%_ip)
			self.startThread(self._o, run)
		else:
			cui.i('Not proxy to checking..')
	def startThread(self, arr, func):
		__q = Queue.Queue()
		__t = []
		for ip in arr:
			__q.put(ip)
		for i in range(self._t):
			__t.append(threading.Thread(target = func, args = (__q, )))
		for i in range(self._t):
			__t[i].setDaemon(True)
			__t[i].start()
		for i in range(self._t):
			__t[i].join(timeout = 10)
	def checkPort(self, host, port):
		try:
			_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			_s.settimeout(3)
			_s.connect((host, int(port)))
			_s.close()
			return True
		except:
			return False
	def checkProxy(self, h, p):
		_p = "http://%s:%s"%(h, p)
		_h = urllib2.ProxyHandler({'http': _p})
		_o = urllib2.build_opener(_h, urllib2.HTTPHandler)
		try:
			_r = _o.open('http://www.baidu.com/img/baidu_jgylogo3.gif', timeout = 5)
			_l = len(_r.read())
			if _l == 705:
				return True
			return False
		except Exception,e:
			return False
	def result(self):
		if len(self._r) > 0:
			cui.i('Scan result:')
			for _r in self._r:
				print "\t%s:%s"%(_r, self._p)
			if self._s != '':
				_f = open(self._s, 'a')
				for _r in self._r:
					_f.write('%s:%s\n'%(_r, self._p))
				_f.close()
				cui.s('Save as (%s)'%self._s)
		else:
			cui.i('Not result!')
		exit(0)
	def banner(self):
		return '''\
	______                    _____                                 
	| ___ \                  /  ___|                                
	| |_/ / __ _____  ___   _\ `--.  ___ __ _ _ __  _ __   ___ _ __ 
	|  __/ '__/ _ \ \/ / | | |`--. \/ __/ _` | '_ \| '_ \ / _ \ '__|
	| |  | | | (_) >  <| |_| /\__/ / (_| (_| | | | | | | |  __/ |   
	\_|  |_|  \___/_/\_\\\\__, \____/ \___\__,_|_| |_|_| |_|\___|_|   
	                     __/ |                                      
	                    |___/                                       '''
	def usage(self):
		cor.p(self.banner(), cor.RED)
		cor.p('PS 1.0 (Proxy Scanner)', cor.GREEN)
		cor.p('\tAuthor: Holger', cor.YELLOW)
		cor.p('\tModify: 2014/11/27', cor.YELLOW)
		cor.p('\tGitHub: https://github.com/h01/ProxyScanner', cor.YELLOW)
		cor.p('\tMyBlog: http://ursb.org', cor.YELLOW)
		cor.p('\tVersion: 1.0', cor.RED)
		cor.p('Usage: ./ps [args] [value]', cor.GREEN)
		cor.p('Args: ', cor.PURPLE)
		cor.p('\t-v --version\t\tPS version')
		cor.p('\t-h --help\t\tHelp menu')
		cor.p('\t-i --ips\t\tIPS: 192.168.1.1-192.168.1.100')
		cor.p('\t-p --port\t\tProxy port (default:8080)')
		cor.p('\t-t --thread\t\tScan thread (default:10)')
		cor.p('\t-s --save\t\tSave scan result')
		exit(0)
	def version(self):
		cui.i('ProxyScanner version 1.0')
		exit(0)