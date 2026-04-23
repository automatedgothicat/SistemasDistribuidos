import socket
import pickle
import threading
import math

# Lista do servidor
class DBList:
    def __init__(self):
        self.value = []

    def append(self, data):
        self.value.extend(data)
        return self

    def remove(self, data):
        self.value.remove(data)
        return self

    def count(self, data):
        temp = len(data)
        print(f"{temp} elemento(s) inserido(s)")
        total = len(self.value)
        print(f"{total} elementos no vetor")
        return total

class Log:
    def __init__(self):
        self.value = []

    def append(self, data):
        self.value.extend(data)
        return self

class Server:
    def __init__(self, host='localhost', port=5000):
        self.dbList = DBList()
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(10)
        self.log = Log()
        print(f"Servidor ouvindo em {self.host}:{self.port}")

    def add(self, data):
        return sum(data)

    def multiply(self,data):
        return math.prod(data)

    def handle_client(self, conn, addr):
        print(f"Cliente conectado: {addr}")
        id = 0
        while True:
            try:
                data = conn.recv(4096)
                if not data:
                    break

                op, params = pickle.loads(data)
                id += 1
                self.log.append([id, self.host, self.port, self.dbList.value, op, params])

                if op == "APPEND":
                    self.dbList.append(params)
                    conn.send(pickle.dumps(self.dbList.value))
                if op == "COUNT":
                    conn.send(pickle.dumps(self.dbList.count(params)))
                if op == "REMOVE":
                    self.dbList.remove(params)
                    print(f"{params} removido")
                    conn.send(pickle.dumps(self.dbList.value))
                if op == "ADD":
                    conn.send(pickle.dumps(self.add(params)))
                if op == "MULTIPLY":
                    conn.send(pickle.dumps(self.multiply(params)))
            except Exception as e:
                print("Erro:", e)
                break

        conn.close()
        print(f"Log da chamada: {self.log.value}")
        print(f"Cliente desconectado: {addr}")

    def run(self):
        try:
            while True:
                conn, addr = self.sock.accept()
                threading.Thread(
                    target=self.handle_client,
                    args=(conn, addr),
                    daemon=True
                ).start()
        except KeyboardInterrupt:
            print("\nEncerrando servidor...")
        finally:
            self.sock.close()
            print("Socket do servidor fechado.")

if __name__ == "__main__":
    server = Server()
    server.run()