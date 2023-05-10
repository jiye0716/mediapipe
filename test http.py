import requests
url = "http://192.168.0.118:80"

data = {'l_elbow': '1'}
response = requests.post(url, data=data)
print(response.text)

# import socket

# HOST = '172.20.10.10'  # Replace with the IP address of ESP32
# PORT = 80  # The port used by the server

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.connect((HOST, PORT))
#     s.sendall(b'Hello, ESP32!')
#     data = s.recv(1024)

# print('Received', repr(data))
