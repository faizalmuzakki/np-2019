# Import module
import socket
from threading import Thread
import glob

files = glob.glob("*")

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((socket.gethostname(), 9000))

def listFiles(ip, port):
	addr = (ip, port)
	sock.sendto('start_ls', addr)
	for filename in files:
		sock.sendto(filename, addr)
	sock.sendto('stop_ls', addr)

def downloadFiles(name, addr):
	ip, port = addr
	if name in files:
		sock.sendto('start_download', addr)
		sock.sendto(str(port)+'_'+name, addr)
		file = open(name, 'rb')
		file_data = file.read()
		for byte in file_data:
			sock.sendto(byte, addr)
		sock.sendto('stop_download', addr)

def server():
	command = ["hello", "ls", "download"]
	while True:
		print "waiting for request"
		data, addr = sock.recvfrom(1024)
		ip, port = addr
		data = str(data).split(' ')
		print "{} from client {}".format(data[0], str(port))
		if data[0] == 'hello':
			print "connection from {}:{}".format(ip, str(port))
			sock.sendto('hello', addr)
		elif data[0] == "ls":
			thread = Thread(target=listFiles, args=(addr))
			thread.start()
		elif data[0] == 'download':
			try:
				filename = data[1]
				thread = Thread(target=downloadFiles, args=(filename, addr))
				thread.start()
			except:
				sock.sendto('error', addr)
		elif data[0] not in command:
			sock.sendto('error', addr)

server()
