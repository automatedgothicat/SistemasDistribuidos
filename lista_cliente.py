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

    def count(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.host, self.port))
            msg = ("COUNT")
            sock.send(pickle.dumps(msg))
            result = pickle.loads(sock.recv(4096))
            return result

    def remove(self, data):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.host, self.port))
            msg = ("REMOVE", data)
            sock.send(pickle.dumps(msg))
            result = pickle.loads(sock.recv(4096))
            return result
            
    def add(self, data):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.host, self.port))
            msg = ("ADD", data)
            sock.send(pickle.dumps(msg))
            result = pickle.loads(sock.recv(4096))
            return result
    
    def multiply(self, data):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.host, self.port))
            msg = ("MULTIPLY", data)
            sock.send(pickle.dumps(msg))
            result = pickle.loads(sock.recv(4096))
            return result

if __name__ == "__main__":
    client = Client()
    x = list(map(int, input("Escreva os numeros na mesma linha: ").split()))
    resultado = client.append(x)
    soma = client.add(x)
    produto = client.multiply(x)
    num = client.count()

    y = input("Escreva um numero para remover: ")
    removed = cliente.remove(y)

    print("Lista recebida do servidor:", resultado)
    print("Soma da lista recebida do servidor:", soma)
    print("Produto da lista recebida do servidor:", produto)
    print("Contagem da lista recebida do servidor:", num)
    print("Lista recebida do servidor após remoção:", removed)