from httplib import *
import re
import config

def uopen(url):
	try:
		pre = url.find('://') + 3
		div = url.find('/', pre)
		left = url[pre:div]
		right = url[div:]
		conn = HTTPSConnection(left)#, timeout = 240)
		#headers = {'User-Agent': 'Firefox/55.0', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
		conn.request('GET', right)#, None, headers)
		re = conn.getresponse().read()
	except:
		if isinstance(conn, HTTPSConnection):
			conn.close()
			del conn
			raise
	conn.close()
	del conn
	return re

def retrieve(url, path):
	content = uopen(url)
	file = open(path, 'wb')
	file.write(content)
	file.close()

def split(last, first):
	list = []
	temp = []
	step = (first-last) / config.number_of_threads + 1
	i = last
	while i < first + 1:
		for j in range(step):
			if  i+j > first:
				break
			temp.append(i + j)
		list.append(temp)
		i += step
		temp = []
	return list

def getid(str, last):
	list = re.compile('p[0-9]{6}').findall(str)
	id_list = []
	for i in list:
		if int(i[1:]) > last:
			id_list.append(i[1:])
	return id_list

# Experimental function
def getcount(str, tag):
	lenth = len(tag) * 2
	tag = re.compile('[a-zA-Z0-9_]{1,}').findall(tag)[0]
	pat = re.compile('tags=%s[\s\S]{1,%d}</a> <span class="post-count">[0-9]{1,6}'%(tag, lenth)).findall(str)
	if pat == []:
		return 0
	list = re.compile('[0-9]{1,6}').findall(pat[0])
	count = int(list[len(list) - 1])
	return count

# <>/\|:"*?
def filter(s):
	tmp = s
	tmp = tmp.replace('?', '_')
	tmp = tmp.replace('/', '_')
	tmp = tmp.replace('\\', '_')
	tmp = tmp.replace('*', '_')
	tmp = tmp.replace('"', '_')
	tmp = tmp.replace('<', '_')
	tmp = tmp.replace('>', '_')
	tmp = tmp.replace('|', '_')
	tmp = tmp.replace(':', '_')
	return tmp

def isexplicit(title):
	for tag in config.taglist:
		if title.find(tag) != -1:
			return True
	return False