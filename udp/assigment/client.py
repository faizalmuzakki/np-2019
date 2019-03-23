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
		self.iter = no
		self.file = open('receive'+str(self.iter)+'.jpg', 'wb')
		threading.Thread.__init__(self)

	def run(self):
		host = socket.gethostname()
		port = 9000
		self.my_socket.connect((host, port))
		data = self.my_socket.recv(32)
		print "Receiving... ",self.iter
		while(data):
			self.file.write(data)
			# time.sleep(.01)
			data = self.my_socket.recv(32)
		self.file.close()
		print "Done Receiving ",self.iter
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
