# Import module
from socket import *
import socket
import threading
import thread
import time
import sys

class Client(threading.Thread):
	def __init__(self, no):
		self.my_socket = socket.socket()
		threading.Thread.__init__(self)
		self.no = no

	def run(self):
		host = socket.gethostname()
		port = 9000
		self.my_socket.connect((host, port))
		with open('file.jpg', 'rb') as file:
			print 'Sending... ',self.no
	        	l = file.read(1024)
        		while (l):
				print 'Sending...',self.no
				self.my_socket.send(l)
				l = file.read(1024)
			file.close()
			print "Done Sending ",self.no
		self.my_socket.shutdown(socket.SHUT_WR)
		self.my_socket.close()

def main():
	client1 = Client(1)
	client2 = Client(2)
	client3 = Client(3)
	client4 = Client(4)

	client1.start()
	client2.start()
	client3.start()
	client4.start()

if __name__=="__main__":
	main()
