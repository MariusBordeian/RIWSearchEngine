# import urllib
import socket
import sys

import urlparse
import requests
import re
import os

"""
url = '192.168.243.80:80'
headers = { 'User-Agent' :  'CLIENT RIW',
			'Connection' :  'close' }

f = urllib.urlopen(url)
print f.read()
"""

# socket.setdefaulttimeout = 0.50
# os.environ['no_proxy'] = '127.0.0.1,localhost'
# linkRegex = re.compile('<a\s*href=[\'|"](.*?)[\'"].*?>')


def OPTIONS(HOST, path='/', PORT=80):
	opt = re.compile('Allow.*(GET).*')
	request_str = 'options ' + path + ' HTTP/1.1 \r\nuser-agent: MyAwesomeCrawler\r\nconnection: close\r\n\r\n'
	# url = urlparse.urlparse(HOST)
	# path = url.path
	# if path == "":
		# path = "/"
	# HOST = url.netloc  # The remote host
	# create an INET, STREAMing socket
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(0.30)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	# s.setblocking(0)
	s.connect((HOST, PORT))
	# s.send("GET / HTTP/1.1%s" % ('\r\n\r\n'))
	s.send(request_str)
	data = (s.recv(1000000))
	# print(data)
	# https://docs.python.org/2/howto/sockets.html#disconnecting
	s.shutdown(1)
	s.close()
	# print('Received', repr(data))
	r = requests.options('http://' + HOST + path, headers={'user-agent':'CLIENT RIW'})
	print(r.headers)
	return 1 if re.search(opt, str(r.headers)) else 0


def GET(HOST, path='/', PORT=80):
	request_str = 'GET ' + path + ' HTTP/1.0\r\nuser-agent: MyAwesomeCrawler\r\nconnection: close\r\n\r\n'
	# url = urlparse.urlparse(HOST)
	# path = url.path
	# if path == "":
		# path = "/"
	# HOST = url.netloc  # The remote host
	# create an INET, STREAMing socket
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(0.30)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	# s.setblocking(0)
	s.connect((HOST, PORT))
	# s.send("GET / HTTP/1.1%s" % ('\r\n\r\n'))
	s.send(request_str)
	data = (s.recv(1000000))
	# print(data)
	# https://docs.python.org/2/howto/sockets.html#disconnecting
	s.shutdown(1)
	s.close()
	# print('Received', repr(data))
	r = requests.get('http://' + HOST + path, headers={'user-agent':'CLIENT RIW'})
	print(r.headers)


def main(argv):
	"""
	HOST = '192.168.243.80'
	PORT = 80
	s = None
	for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM):
		af, socktype, proto, canonname, sa = res
		try:
			s = socket.socket(af, socktype, proto)
		except socket.error as msg:
			s = None
			continue
		try:
			s.connect(sa)
		except socket.error as msg:
			s.close()
			s = None
			continue
		break
	if s is None:
		print('could not open socket')
		sys.exit(1)
	s.sendall('get /riw/ http/1.1\r\nhost: 192.168.243.80\r\nuser-agent: CLIENT RIW\r\nconnection: close')

	while 1:
		response = s.recv(8192)
		print(response)
		if not response: break
	s.close()
	"""
	print(OPTIONS('www.steuerhaus.com'))
	# print(OPTIONS('www.rdf.ro'))
	# print(OPTIONS('www.ace.tuiasi.ro'))
	# GET('172.217.16.163')
	# GET('176.223.194.68')
	# GET('www.rdf.ro')


if __name__ == "__main__":
	main(sys.argv[1:])

"""
dest = 'http://192.168.243.80'
port = 80

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

sock.connect((dest,port))
sock.sendall("get /riw/ http/1.1\r\nhost: 192.168.243.80\r\nuser-agent: CLIENT RIW\r\nconnection: close".bytes())
response = sock.recv(8192)
length = struct.unpack("!H",bytes(response[:2]))[0]
while len(response) - 2 < length:
	response += sock.recv(8192)
sock.close()
response = response[2:]
"""
