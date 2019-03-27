# Import module
from socket import *
import socket
import threading
import sys
import os
from ast import literal_eval

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 9000
sock.connect((host, port))

name = raw_input('your name: ')
while True:
	command = raw_input('your command: ')
	if command[0] == "exit":
		break

	sock.send(command)
	command = command.split(" ")

	print '\n=========='
	files = ''
	if command[0] == 'ls':
		print "showing files"
		print '============='

		data = sock.recv(1024)
		files = literal_eval(data)

		for filename in files:
			print filename

	elif command[0] == 'download':
		if len(command) == 2:
			print "downloading files"
			print '================='

			filename = name+'_'+command[1]
			file = open(filename, 'wb')
			data = sock.recv(1024)
			while data:
				print "downloading block: ", data
				file.write(data)
				data = sock.recv(1024)
			file.close()
			print "done receiving", filename

		else:
			print "syntax error"

	else:
		print "command not found"

	print '==========\n'
sock.close()
