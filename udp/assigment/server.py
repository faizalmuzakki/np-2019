# Import module
from socket import *
import socket
import threading
import thread
import time
import sys

class ProcessTheClient(threading.Thread):
	def __init__(self, connection, address):
		self.connection = connection
		self.address = address
		threading.Thread.__init__(self)

	def run(self):
		while True:
			with open('file.jpg', 'rb') as file:
				print 'Sending... ',self.address
		        	l = file.read(1024)
	        		while (l):
					print 'Sending...',self.address
					self.connection.send(l)
					l = file.read(1024)
				file.close()
				print "Done Sending ",self.address
			self.connection.send("Thank you for connecting")
			self.connection.close()
			break

class Server(threading.Thread):
	def __init__(self):
		self.the_clients = []
		self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		threading.Thread.__init__(self)

	def run(self):
		host = socket.gethostname()
		port = 9000
		self.my_socket.bind((host, port))
		self.my_socket.listen(1)
		while True:
			self.connection, self.client_address = self.my_socket.accept()
			print >> sys.stderr, 'connection from', self.client_address

			clt = ProcessTheClient(self.connection, self.client_address)
			clt.start()

			self.the_clients.append(clt)

def main():
	svr = Server()
	svr.start()

if __name__=="__main__":
	main()
