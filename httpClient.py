# import urllib
import socket
import sys

"""
url = '192.168.243.80:80'
headers = { 'User-Agent' :  'CLIENT RIW',
			'Connection' :  'close' }

f = urllib.urlopen(url)
print f.read()
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