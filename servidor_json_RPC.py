import socket
import json
import threading

# Lista do servidor
class DBList:
    def __init__(self):
        self.value = []

    def append(self, data):
        self.value.extend(data)
        return self.value

class Server:
    def __init__(self, host='localhost', port=5000):
        self.dbList = DBList()
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)
        print(f"Servidor ouvindo em {self.host}:{self.port}")

    # função para tratar cada cliente conectado
    def handle_client(self, conn, addr):
        print(f"Conexão de {addr}") # addr: endereço vinculado ao soquete na outra extremidade da conexão
        data = conn.recv(1024).decode("utf-8")  # recebe bytes
        request = json.loads(data)  # desserializa
        print("Servidor recebeu:", request)

        # Executa a operação
        if request["operation"] == "append":
            result = self.dbList.append(request["data"])
        else:    
            result = {"erro": "Operação desconhecida"}
        
        response = json.dumps(result).encode("utf-8")
        conn.sendall(response)
        conn.close()
        
    def start_server(self):
        while True:
            conn, addr = self.sock.accept()
            threading.Thread(
                target=self.handle_client, 
                args=(conn, addr), 
                daemon=True
            ).start()

if __name__ == "__main__":
    server = Server()
    server.start_server()