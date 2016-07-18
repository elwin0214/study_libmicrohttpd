import socket
import sys

port=9000
host="127.0.0.1"
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
try:
    s.connect((host,port))
except:
    print 'connect error'
s.send("GET / HTTP/1.1\r\n\r\n")
s.shutdown(socket.SHUT_WR)
print 'send finished.'
while 1:
    buf=s.recv(4096)
    if not len(buf):
        break
    #print buf
    sys.stdout.write(buf)
    