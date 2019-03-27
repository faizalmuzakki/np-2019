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
		threading.Thread.__init__(self)

	def run(self):
		host = socket.gethostname()
		port = 9000
		while True:
			command = raw_input('your command: ')
			if command == "exit":
				break

			self.my_socket.sendto(command, (host, port))

			data, addr = self.my_socket.recvfrom(1024)
			print '=========='
			if str(data) == 'start_ls':
				print 'showing all files'
				print '=========='
				while True:
					data, addr = self.my_socket.recvfrom(1024)
					if str(data) == 'stop_ls':
						break
					else:
						print data
			elif str(data) == 'start_download':
				data, addr = self.my_socket.recvfrom(1024)
				print "now downloading ", str(data)
				filename = str(data)
				print '=========='
				file = open(data, 'wb+')
				while True:
					if str(data) == 'stop_download':
						break
					print "downloading progress ", str(data)
					data, addr = self.my_socket.recvfrom(1024)
					file.write(data)
				file.close()
			elif str(data) == 'error':
				print "command not found"
			else:
				print str(data)
			print '==========\n'
		self.my_socket.close()

def main():
	client1 = Client(1)
	# client2 = Client(2)
	# client3 = Client(3)
	# client4 = Client(4)

	client1.start()
	# client2.start()
	# client3.start()
	# client4.start()

if __name__=="__main__":
	main()
