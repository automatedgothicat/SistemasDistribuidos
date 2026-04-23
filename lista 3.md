  
## *Exercício 1*. Explique a diferença entre comunicação síncrona e assíncrona em sistemas distribuídos. Dê exemplos de uso prático.  
A diferença entre comunicação síncrona e assíncrona é que a primeira precisa ser feita em uma ordem correta, de forma linear, formando uma fila para que as mensagens sejam recebidas e enviadas, enquanto a comunicação assíncrona não precisa ser linear, fazendo com que cada mensagem seja executada separadamente, sem bloquear o servidor para o recebimento de novas mensagens enquanto executa aquela tarefa. A comunicação síncrona é suficiente para comunicação entre um cliente e um servidor, mas a assíncrona pode ser utilizada quando o cliente precisa contatar vários servidores simultaneamente.
## *Exercício 2*. Implemente uma versão simplificada de RPC onde um cliente envia dois números e o servidor retorna a soma.  
```cliente.py
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
            
    def add(self, data):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.host, self.port))
            msg = ("ADD", data)
            sock.send(pickle.dumps(msg))
            result = pickle.loads(sock.recv(4096))
            return result

if __name__ == "__main__":
    client = Client()
    resultado = client.append([2, 3])
    print("Lista recebida do servidor:", resultado)
```

```servidor.py
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

    def add(self, data):
        return sum(data)

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

                if op == "ADD":
                    conn.send(pickle.dumps(self.add(params)))
                    
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
```
## *Exercício 3*. Modifique o código apresentado para suportar operação de multiplicação além do append.  
```cliente.py
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
    print("Lista recebida do servidor:", resultado)
    print("Soma da lista recebida do servidor:", soma)
    print("Produto da lista recebida do servidor:", produto)
```

```servidor.py
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

class Server:
    def __init__(self, host='localhost', port=5000):
        self.dbList = DBList()
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)
        print(f"Servidor ouvindo em {self.host}:{self.port}")

    def add(self, data):
        return sum(data)
        
    def multiply(self,data):
        return math.prod(data)

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

                if op == "ADD":
                    conn.send(pickle.dumps(self.add(params)))
                    
                if op == "MULTIPLY":
                    conn.send(pickle.dumps(self.multiply(params)))
                    
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
```
## *Exercício 4*. Proponha uma modificação no código para que o servidor registre logs de cada chamada de cliente.    
```cliente.py
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

    print("Lista recebida do servidor:", resultado)
    print("Soma da lista recebida do servidor:", soma)
    print("Produto da lista recebida do servidor:", produto)
```
```servidor.py
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
        self.sock.listen(5)
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
                if op == "ADD":
                    conn.send(pickle.dumps(self.add(params)))
                if op == "MULTIPLY":
                    conn.send(pickle.dumps(self.multiply(params)))

                print(f"Log da chamada: {self.log.value}")
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
```
## *Exercício 5*. Modifique a classe DBList para adicionar os métodos remove(data) e count(). Depois, adapte cliente e servidor para que essas operações também possam ser chamadas remotamente via RPC.
```cliente.py

```
```servidor.py
```