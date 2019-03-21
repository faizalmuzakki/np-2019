# Import module
from socket import *
import socket
import threading
import thread
import time
import sys

class ProcessTheClient(threading.Thread):
	def __init__(self, connection, address, iter):
		self.iter = iter
		self.file = open('receive'+str(self.iter)+'.jpg', 'wb')
		self.connection = connection
		self.address = address
		threading.Thread.__init__(self)

	def run(self):
		while True:
			data = self.connection.recv(32)
			print "Receiving... ",self.iter
			while(data):
				self.file.write(data)
				# time.sleep(.01)
				data = self.connection.recv(32)
			self.file.close()
			print "Done Receiving ",self.iter
			self.connection.send("Thank you for connecting")
			self.connection.close()
			break

class Server(threading.Thread):
	def __init__(self):
		self.the_clients = []
		self.my_socket = socket.socket()
		threading.Thread.__init__(self)

	def run(self):
		host = socket.gethostname()
		port = 9000
		self.my_socket.bind((host, port))
		self.my_socket.listen(1)
		iter = 0
		while True:
			self.connection, self.client_address = self.my_socket.accept()
			if self.connection:
				iter+=1
			print >> sys.stderr, 'connection from', self.client_address, iter

			clt = ProcessTheClient(self.connection, self.client_address, iter)
			clt.start()

			self.the_clients.append(clt)

def main():
	svr = Server()
	svr.start()

if __name__=="__main__":
	main()
