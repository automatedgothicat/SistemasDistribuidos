import socket
import pickle

class Client:
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port

    def append(self, data):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.host, self.port))
            msg = ("APPEND", data)
            sock.send(pickle.dumps(msg))
            result = pickle.loads(sock.recv(4096))
            return result

if __name__ == "__main__":
    client = Client()
    resultado = client.append([1, 2, 3])
    print("Lista recebida do servidor:", resultado)