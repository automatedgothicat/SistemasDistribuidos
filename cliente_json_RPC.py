import socket
import json
import pickle

class Client:
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port

    def append(self, data):
        request = {
            "operation": "append",
            "data": data
        }

        msg = json.dumps(request).encode("utf-8")

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.host, self.port))
            sock.sendall(msg)
            
            response = sock.recv(1024).decode("utf-8")
        return json.loads(response)

if __name__ == "__main__":
    client = Client()
    resultado = client.append([1, 2, 3])
    print("Lista recebida do servidor:", resultado)