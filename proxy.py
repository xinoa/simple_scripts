import sys
import socket
import threading

def request_handler(buff):
	return buff

def response_handler(buff):
	return buff

def receive_from(connection):
	data = b""
	connection.settimeout(2)
	try:
		buff = connection.recv(1024)
		data += buff
		while len(buff) == 1024:
			buff = connection.recv(1024)
			data += buff
	except:
		print("[*] Error: Connection error.")
	return data

def hexdump(buff, length=16):
	results = []
	for i in range(0, len(buff), length):
		s = buff[i:i+length]
		hexa = ' '.join([f'{x:04X}' for x in s])
		text = ''.join([x if 0x20 <= ord(x) < 0x7F else '.' for x in s])
		results.append(f"{i:08X}	{hexa}	{text}")
	print('\n'.join(results))


def proxy_handler(client, r_host, r_port, recv_first):
	remote = socket.socket()
	remote.connect((r_host, r_port))
	if recv_first:
		remote_buffer = receive_from(remote)
		print(f"[<--] Received {len(remote_buffer)} bytes from remote.")
		hexdump(remote_buffer)
		remote_buffer = response_handler(remote_buffer)
		if len(remote_buffer):
			client.send(remote_buffer)
			print(f"[-->] Sent {len(remote_buffer)} bytes to client.")

	while True:
		local_buffer = receive_from(client)
		print(f"[<--] Received {len(local_buffer)} bytes from client.")
		if len(local_buffer):
			hexdump(local_buffer)
			local_buffer = request_handler(local_buffer)
			remote.send(local_buffer)
			print(f"[-->] Sent {len(local_buffer)} bytes to remote.")

		remote_buffer = receive_from(remote)
		print(f"[<--] Received {len(remote_buffer)} bytes from remote.")
		if len(remote_buffer):
			hexdump(remote_buffer)
			remote_buffer = response_handler(remote_buffer)
			client.send(remote_buffer)
			print(f"[-->] Sent {len(remote_buffer)} bytes to client.")

		if not len(local_buffer) or not len(remote_buffer):
			client.close()
			remote.close()
			print('[*] Info: No more data. Closing connections.')
			break

def server_loop(l_host, l_port, r_host, r_port, recv_first):
	server = socket.socket()
	try:
		server.bind((l_host, l_port))
	except:
		print("[*] Error: Failed to start the server.")
		sys.exit(0)

	server.listen(5)
	print(f"[*] Info: Listening on {l_host}:{l_port}")
	while True:
		proxy, addr = server.accept()
		print(f"[*] Info: Accepted connection from {addr[0]}:{addr[1]}")
		proxy_thread = threading.Thread(target=proxy_handler, args=(proxy, r_host, r_port, recv_first))
		proxy_thread.start()

def main():
	if len(sys.argv[1:]) != 5:
		print("Usage: ./proxy.py [localhost] [localport] [remotehost] [remoteport] [receivefirst]")
		print("Example: ./proxy.py 127.0.0.1 9000 10.12.132.1 9000 True")
		sys.exit(0)

	l_host = sys.argv[1]
	l_port = int(sys.argv[2])
	r_host = sys.argv[3]
	r_port = int(sys.argv[4])
	recv_first = True if "True" in sys.argv[5] else False

	server_loop(l_host, l_port, r_host, r_port, recv_first)

if __name__ == "__main__":
	main()
