#406800

from urllib import unquote
import os, sys, threading, traceback
import config
from functions import *

def down(*list):
	for i in list:
		try:
			page = uopen('https://yande.re/post/show/%d'%i)
			left = page.find('id="highres" href="') + 19
			if left == -1:
				raise
			right = page.find('">Download', left)
			if right == -1:
				right = page.find('">Image (', left)
			if right == -1:
				raise
			url = page[left:right]
			pos = url.find('/yande.re') + 1
			title = filter(unquote(url[pos:]))
			if (not config.allow_exp) and isexplicit(title):
				continue
			retrieve(url, '%s%s'%(config.index_path, title))
			print '%d Downloaded'%i

		except:
			try:
				if page.find('This post was deleted.') != -1:
					print '%s was deleted'%i
					continue
			except:
				pass
			print '%d not downloaded'%i
			os.system('echo %d>> %serrlog.txt'%(i, config.index_path))
			continue

def main():
	thisF = open(sys.argv[0], 'r+')
	lastStr = thisF.readline()
	last = int(lastStr[1:-1]) + 1
	print 'Starting from %d'%last
	if not os.path.exists(config.index_path):
		os.mkdir(config.index_path)

	try:
		index = uopen('https://yande.re/post')
		left = index.find('class="plid">#pl') + 17
		right = index.find('</span>', left)
		url = index[left:right]
		first = int(url[-6:])
		#first = 405786
		print 'To %d'%first
		_max = max(first, last)
		threads = []
		list = split(last, first)
		for i in list:
			t = threading.Thread(target = down, args = (i))
			t.setDaemon(True)
			t.start()
			threads.append(t)
		for i in range(len(list)):
			threads[i].join()
	except KeyboardInterrupt:
		print 'Exiting now'
		exit()
	except:
		traceback.print_exc()
		print 'Connection failed'
		exit()

	print 'Already up-to-date'
	thisF.seek(0)
	thisF.write('#%d'%_max)
	return

if __name__ == '__main__':
	main()