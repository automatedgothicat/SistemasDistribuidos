import socket

HOST = "127.0.0.1"
PORT = 5001


def consultar_produto():
    nome_produto = input("Informe o nome do produto: ").strip()

    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((HOST, PORT))

    cliente.sendall(nome_produto.encode("utf-8"))

    resposta = cliente.recv(1024).decode("utf-8")
    print("\nResposta do servidor:")
    print(resposta)

    cliente.close()


if __name__ == "__main__":
    consultar_produto()