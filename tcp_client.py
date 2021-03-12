HOST = "127.0.0.1"
PORT = 8080

REQUEST = (
	b"GET / HTTP/1.1\r\n"
	b"Host: example.com\r\n"
	b"\r\n"
)

import socket

def main():
	client = socket.socket()
	client.connect((HOST, PORT))
	client.send(REQUEST)
	response = b""
	chunk = client.recv(1024)
	response += chunk
	while len(chunk) == 1024:
		chunk = client.recv(1024)
		response += chunk

	print(str(response))
	client.close()

if __name__ == "__main__":
	main()
