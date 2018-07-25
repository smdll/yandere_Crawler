from urllib import unquote
import os, sys, threading, traceback
import config
from functions import *

tag = ''

def down(*list):
	global tag
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
			retrieve(url, '%s%s\\%s'%(config.tag_path, tag, title))
			print '%s Downloaded'%i
		except:
			print '%s not downloaded'%i
			os.system('echo %s>> %s%s\\errlog.txt'%(i, config.tag_path, tag))
			continue

def main():
	global tag
	tail = last = 1
	taglist = []
	tag = raw_input('Tag to sync(leave empty to sync all):')
	if tag == '':
		templist = open('%slist.txt'%config.tag_path, 'r').readlines()
		for i in templist:
			taglist.append(i[:-1])
	else:
		taglist.append(tag)
	for tag in taglist:
		print 'Syncing %s'%tag
		if not os.path.exists('%s%s'%(config.tag_path, tag)):
			os.mkdir('%s%s'%(config.tag_path, tag))
		if os.path.exists('%s%s\\last.txt'%(config.tag_path, tag)):
			file = open('%s%s\\last.txt'%(config.tag_path, tag), 'r+')
			last = int(file.readline()[:-1])
			print 'Last:%d'%last
			tail = last
			file.close()

		page = 1
		index = uopen('https://yande.re/post?tags=%s&page=%d'%(tag, page))
		print '%d in total'%getcount(index, tag) # Buggy
		if not index.find('Nobody here but us chickens!') == -1:
			print 'Invalid tag'
			os.system('rmdir /Q %s\\%s'%(config.tag_path, tag))
			continue
		while True:
			try:
				index = uopen('https://yande.re/post?tags=%s&page=%d'%(tag, page))
				arr = getid(index, last)
				if len(arr) == 0:
					break
				tail = max(int(arr[0]), last, tail)
				page += 1
				list = []
				for i in range(config.number_of_threads):
					list.append(arr[i * len(arr) / config.number_of_threads:(i + 1) * len(arr) / config.number_of_threads])
				threads = []
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
				print 'Connection failed'
				traceback.print_exc()
				input()
				exit()
		print 'Done syncing %s\n'%tag
		if os.path.exists('%s%s\\last.txt'%(config.tag_path, tag)):
			os.system('del /Q %s%s\\last.txt'%(config.tag_path, tag))
		os.system('echo %d>>%s%s\\last.txt'%(tail, config.tag_path, tag))
		f = open('%slist.txt'%config.tag_path).read()
		if f.find(tag) == -1:
			os.system('echo %s>>%slist.txt'%(tag, config.tag_path))
	return

if __name__ == '__main__':
	main()