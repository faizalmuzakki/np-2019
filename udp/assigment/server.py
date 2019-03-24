# Import module
from socket import *
import socket
import threading
import sys

class ProcessTheClient(threading.Thread):
	def __init__(self, connection, address):
		self.connection = connection
		self.address = address
		threading.Thread.__init__(self)

	def run(self):
		file = open('sent.png', 'rb')
		data = file.read()
		print "now sending", self.address
		sent = 0
		for x in data:
		    self.connection.sendto(x, self.address)
		print "done sending", self.address

class Server(threading.Thread):
	def __init__(self):
		self.the_clients = []
		self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		threading.Thread.__init__(self)

	def run(self):
		host = socket.gethostname()
		port = 9000
		self.my_socket.bind((host, port))
		while True:
			data, self.client_address = self.my_socket.recvfrom(1024)
			print >> sys.stderr, 'connection from', self.client_address

			clt = ProcessTheClient(self.my_socket, self.client_address)
			clt.start()

			self.the_clients.append(clt)

def main():
	svr = Server()
	svr.start()

if __name__=="__main__":
	main()
