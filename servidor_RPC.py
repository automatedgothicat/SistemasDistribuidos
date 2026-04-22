import socket
import pickle
import threading

# Lista do servidor
class DBList:
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
        self.sock.listen(5)
        print(f"Servidor ouvindo em {self.host}:{self.port}")

    def handle_client(self, conn, addr):
        print(f"Cliente conectado: {addr}")
        while True:
            try:
                data = conn.recv(4096)
                if not data:
                    break

                op, params = pickle.loads(data)

                if op == "APPEND":
                    self.dbList.append(params)
                    conn.send(pickle.dumps(self.dbList.value))
            except Exception as e:
                print("Erro:", e)
                break

        conn.close()
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