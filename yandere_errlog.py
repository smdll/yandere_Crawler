from urllib import unquote
import os, sys, threading
import config
from functions import *

tag = ''
path = ''

def down(*list):
	global tag
	global path
	for i in list:
		try:
			page = uopen('%s%s'%('https://yande.re/post/show/', i))
			left = page.find('id="highres" href="') + 19
			if left == -1:
				raise
			right = page.find('">Download', left)
			if right == -1:
				right = page.find('">Image (', left)
			if right == -1:
				raise
			if (not config.allow_exp) and isexplicit(title):
				continue
			url = page[left:right]
			pos = url.find('/yande.re') + 1
			title = filter(unquote(url[pos:]))
			retrieve(url, '%s%s'%(path, title))
			print '%s Downloaded'%i

		except:
			try:
				if page.find('This post was deleted.') != -1:
					print '%s was deleted'%i
					continue
			except:
				pass
			print '%s not downloaded'%i
			os.system('echo %s>> %serrlog2.txt'%(i, path))
			continue

def main():
	global tag
	global path
	tag = raw_input('Tag for errlog(leave empty to sync index):')
	if tag == '':
		path = config.index_path
	else:
		path = '%s%s\\'%(config.tag_path, tag)
	if not os.path.exists(path):
		print 'Exiting now'
		exit()
	file = open('%serrlog.txt'%path, 'rt')
	flines = file.readlines()
	file.close()

	arr = []
	for i in flines:
		arr.append(i.rstrip('\n'))
	list = []
	for i in range(config.number_of_threads):
		list.append(arr[i * len(arr) / config.number_of_threads:(i + 1) * len(arr) / config.number_of_threads])

	try:
		threads = []
		for i in list:
			t = threading.Thread(target = down, args = (i))
			t.setDaemon(True)
			t.start()
			threads.append(t)
		for i in range(config.number_of_threads):
			threads[i].join()
	except KeyboardInterrupt:
		print 'Exiting now'
		exit()
	except:
		print 'Connection failed'
		exit()
	print 'Done'
	os.system('del /Q %serrlog.txt'%path)
	os.system('rename %serrlog2.txt errlog.txt'%path)
	return

if __name__ == '__main__':
	main()