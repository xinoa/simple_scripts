import socket

HOST = "127.0.0.1"
PORT = 8080

def hexdump(buff, length=16):
	results = []
	for i in range(0, len(buff), length):
		s = buff[i:i+length]
		hexa = ' '.join([f'{x:04X}' for x in s])
		text = ''.join([f'{x}' if 0x20 <= ord(x) < 0x7F else '.' for x in str(s, 'utf-8')])
		results.append(f"{i:08X}	{hexa}		{text}")
	print('\n'.join(results))

def main():
	server = socket.socket()
	server.bind((HOST, PORT))
	server.listen(5)
	print(f"[*] Info: Server is listening on {HOST}:{PORT}")
	client, addr = server.accept()
	print(f"[*] Info: Accepted connection from {addr[0]}:{addr[1]}")
	request = b""
	chunk = client.recv(1024)
	request += chunk
	while len(chunk) == 1024:
		chunk = client.recv(1024)
		request += chunk

	print(f"[*] Info: Recieved {len(request)} bytes from client:")
	hexdump(request)
	response = b"Hello Client!"
	print("[*] Info: Sending response.")
	client.send(bytes(response))
	client.close()
	server.close()

if __name__ == "__main__":
	main()
