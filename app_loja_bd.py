from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__) # criando a aplicação Flask 

banco = "loja.db"

def conectar():
    conn = sqlite3.connect(banco)
    conn.row_factory = sqlite3.Row  # objeto que representa uma linha de resultado de consulta SQL 
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
        CREATE TABLE IF NOT EXISTS pedido (
            pedido_id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_produto TEXT NOT NULL,
            quantidade_produto INTEGER NOT NULL,
            FOREIGN KEY (nome_produto) REFERENCES produto(nome)          
        )               
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO produto (codigo, nome, quantidade)
        VALUES
        ('CP000001', 'camisa', 10),
        ('CP000002', 'calça', 8),
        ('CP000003', 'vestido', 5)
    """)

    conn.commit()
    conn.close()

@app.route("/")
def tela_inicial():
    return "<p> BEM VINDO AO SD COMPRAS! </p>"

@app.route("/status", methods=["GET"]) 
def status():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) AS total FROM pedido")
    total_pedidos = cursor.fetchone()["total"]

    conn.close()

    return jsonify({
        "mensagem": "Servidor funcionando",
        "total_pedidos": total_pedidos
    })

# retorna o estoque atual
@app.route("/estoque", methods=["GET"])
def consultar_estoque():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT codigo, nome, quantidade FROM produto"
    )
    info = cursor.fetchall()
    conn.close()

    resultado = []
    for i in info:
        resultado.append({
            "codigo": i["codigo"],
            "nome":i["nome"],
            "quantidade":i["quantidade"]
        })

    return jsonify(resultado)

# retorna os pedidos feitos
@app.route("/pedidos", methods=["GET"])
def listar_pedidos():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT pedido_ID, nome_produto, quantidade_produto FROM pedido"
    )
    pedidos = cursor.fetchall()
    conn.close()

    resultado = []
    for p in pedidos:
        resultado.append({
            "pedido_id": p["pedido_ID"],
            "produto": p["nome_produto"],
            "quantidade_comprada": p["quantidade_produto"]
        })

    return jsonify(resultado)

# registra uma compra
@app.route("/comprar", methods=["POST"])
def comprar():
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "JSON não enviado"}),400
        
    produto = dados.get("produto","").strip()
    qtd = dados.get("quantidade")

    if not produto or qtd is None:
        return jsonify({"erro": "Os campos 'produto' e 'quantidade' são obrigatórios!"}), 400

    if qtd <= 0:
        return jsonify({"erro": "Quantidade inválida"}), 400 # 400: servidor não processa a requisição do cliente

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT nome, quantidade FROM produto WHERE nome = ?",(produto,)
    )
    item = cursor.fetchone()

    if item is None:
        conn.close()
        return jsonify({"erro": "Produto não encontrado"}), 404 # 404: rota solicitada não encontrada

    if item["quantidade"] < qtd:
        conn.close()
        return jsonify({"erro": "Estoque insuficiente"}), 400

    cursor.execute(
        "UPDATE produto SET quantidade = quantidade - ? WHERE nome = ?",(qtd,produto)
    )

    cursor.execute(
        "INSERT INTO pedido (nome_produto,quantidade_produto) VALUES (?, ?)",
    (produto, qtd)
    )

    conn.commit()
    conn.close()

    return jsonify ({
        "mensagem": "Pedido realizado!",
        "produto": item["nome"],
        "quantidade_comprada": qtd,
        "em_estoque": item["quantidade"] - qtd
    })

# rodando o servidor Flask
if __name__ == "__main__":
    # flask --app app run
    criar_tabelas()
    app.run() # rodando servidor localmente