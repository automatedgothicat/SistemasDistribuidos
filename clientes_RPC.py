import socket
import pickle
import threading

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

def client_task(data):
    client = Client()
    result = client.append(data)
    print(f"Cliente enviou {data}, lista atual {result}")

if __name__ == "__main__":
    # Emulando dados de diferentes clientes
    clients_data = [
      [1,2,3],
      [4,5],
      [6,7,8,9]
    ]

    # Executa cada cliente em thread separada
    threads = []
    for data in clients_data:
        t = threading.Thread(target=client_task, args=(data,))
        t.start()
        threads.append(t)

    # Esperar todos os clientes terminarem
    for t in threads:
        t.join()