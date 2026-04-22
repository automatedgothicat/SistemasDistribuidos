# Importações necessárias
import queue  # fila
import threading

# Definição da classe que representa uma lista no server
class DBList:
    def __init__(self): # Construtor da classe
        self.value = []

    def append(self, data): # método
        self.value.extend(data)
        return self # retorna a lista atualizada

# Canal de comunicação simples usando fila
class Channel:
    def __init__(self):
        self.client_to_server = queue.Queue()
        self.server_to_client = queue.Queue()

    # Enviar mensagem
    def sendToServer(self, msg):
        self.client_to_server.put(msg)

    def recvFromClient(self):
        return self.client_to_server.get()

    def sendToClient(self, msg):
        self.server_to_client.put(msg)

    def recvFromServer(self):
        return self.server_to_client.get()

# Stub do cliente
class Client:
    def __init__(self, channel): # construtor que recebe o canal de comunicação
        self.channel = channel   # Objeto channel/ Armazena o canal para enviar/receber mensagens.

    def append(self, data, dbList): # “substitui” a chamada real de append do servidor.
        # Cria a mensagem (nome da operação + parâmetros)
        msg = ("APPEND", data, dbList)
        # Envia ao servidor
        self.channel.sendToServer(msg)
        # Espera a resposta
        result = self.channel.recvFromServer()
        return result

# Servidor que processa a mensagem
class Server:
    def __init__(self, channel): # construtor que recebe o canal de comunicação
        self.channel = channel   # Armazena o canal para enviar/receber mensagens.
        self.dbList = DBList()   # Inicializa a lista “remota” do servidor.

    def append(self, data, dbList):
        return dbList.append(data)

    def run(self):
        while True:
            msg = self.channel.recvFromClient()
            op, data, dbList = msg
            if op == "APPEND":
                result = self.append(data, dbList)
                self.channel.sendToClient(result)

# Função para rodar o servidor em thread separada
def start_server(server):
    server.run()

# Criar o canal de comunicação
channel = Channel()

# Criar servidor e rodar em thread separada
server = Server(channel)
server_thread = threading.Thread(target=start_server, args=(server,), daemon=True)
server_thread.start()

# Criar cliente
client = Client(channel) # Cria o cliente que se comunica pelo canal.

db_list = DBList() # cria a lista a ser manipulada
# Chamada RPC
result = client.append([1, 2, 3], db_list)

print("Lista no cliente após append:", result.value)

