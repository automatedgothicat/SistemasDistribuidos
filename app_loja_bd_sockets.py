import socket
import sqlite3

HOST = "127.0.0.1"
PORT = 5001
BANCO = "loja.db"


def conectar():
    conn = sqlite3.connect(BANCO)
    conn.row_factory = sqlite3.Row
    return conn


def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produto (
            codigo TEXT PRIMARY KEY,
            nome TEXT NOT NULL UNIQUE,
            quantidade INTEGER NOT NULL
        )
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO produto (codigo, nome, quantidade)
        VALUES
        ('CP000001', 'camisa', 10),
        ('CP000002', 'calca', 8),
        ('CP000003', 'vestido', 5)
    """)

    conn.commit()
    conn.close()


def consultar_produto(nome_produto):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT nome, quantidade FROM produto WHERE nome = ?",
        (nome_produto,)
    )
    item = cursor.fetchone()
    conn.close()

    return item


def iniciar_servidor():
    criar_tabelas()

    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((HOST, PORT))
    servidor.listen()

    print(f"Servidor aguardando conexões em {HOST}:{PORT}...")

    while True:
        conn, endereco = servidor.accept()
        print(f"Cliente conectado: {endereco}")

        try:
            dados = conn.recv(1024).decode("utf-8").strip()

            if not dados:
                resposta = "Erro: nenhum nome de produto foi enviado."
            else:
                item = consultar_produto(dados)

                if item is None:
                    resposta = f"Erro: produto '{dados}' não encontrado."
                else:
                    resposta = (
                        f"Produto: {item['nome']} | "
                        f"Quantidade em estoque: {item['quantidade']}"
                    )

            conn.sendall(resposta.encode("utf-8"))

        except Exception as e:
            mensagem_erro = f"Erro no servidor: {e}"
            conn.sendall(mensagem_erro.encode("utf-8"))

        finally:
            conn.close()
            print(f"Conexão encerrada com {endereco}")


if __name__ == "__main__":
    iniciar_servidor()