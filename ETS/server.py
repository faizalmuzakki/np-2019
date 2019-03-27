# Import module
import socket
from threading import Thread
import glob


command = ["ls", "download"]
files = glob.glob("*")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((socket.gethostname(), 9000))
sock.listen(1)

def downloadFiles(conn, name, addr):
	ip, port = addr
	if name in files:
		with open(name, 'rb') as file:
			print 'Sending... ', addr
			bytes = file.read(1024)
			while (bytes):
				print 'Sending...', addr
				conn.send(bytes)
				bytes = file.read(1024)
		file.close()

class ProcessTheClient(Thread):
	def __init__(self, connection, address):
		self.connection = connection
		self.address = address
		Thread.__init__(self)

	def run(self):
		while True:
			data = self.connection.recv(1024)
			ip, port = self.address
			data = str(data).split(' ')
			print "{} from client {}".format(data[0], str(port))

			if data[0] == "ls":
				self.connection.send(str(files))

			elif data[0] == 'download':
				if len(data) == 2:
					filename = data[1]
					downloadFiles(self.connection, filename, self.address)
				else:
					print "syntax error"

			elif data[0] not in command:
				self.connection.send('error')

def server():
	while True:
		print "waiting for request"
		conn, addr = sock.accept()
		clt = ProcessTheClient(conn, addr)
		clt.start()

server()
