# Import module
from socket import *
import socket
import threading
import sys
import os

class Client(threading.Thread):
	def __init__(self, no):
		self.iter = no
		self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.file = open('received'+str(self.iter)+'.jpg', 'wb+')
		threading.Thread.__init__(self)

	def run(self):
		host = socket.gethostname()
		port = 9000
		self.my_socket.sendto('ini data', (host, port))
		self.my_socket.settimeout(2)
		received = 0
		while True:
			try:
				data, addr = self.my_socket.recvfrom(1024)
				self.file.write(data)
				received += 1
			except timeout:
				break
		size = os.stat('file.jpg').st_size
		print "\r client {} sent {} of {} " . format(self.iter, received, size)
		self.file.close()
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
