from flask import Flask, request, jsonify
from threading import Lock

app = Flask(__name__)

lock_banco = Lock()

# "Banco" em memória
banco = {
    "produtos": {
        "camisa": {"codigo": "CP000001", "nome": "camisa", "quantidade": 10},
        "calca": {"codigo": "CP000002", "nome": "calca", "quantidade": 8},
        "vestido": {"codigo": "CP000003", "nome": "vestido", "quantidade": 5}
    },
    "pedidos": [],
    "proximo_pedido_id": 1
}

# Pagina inicial
@app.route("/") # app.route: ligar uma URL (rota) a uma função do Flask
def home():
    return "Bem vindo ao SD Vestuário!"

# Retorna com a informação de servidor funcionando e quantos pedidos possui.
@app.route("/status", methods=["GET"]) # app.route: ligar uma URL (rota) a uma função do Flask
def status():
    with lock_banco:
        total_produtos = len(banco["produtos"])
        total_pedidos = len(banco["pedidos"])

    return jsonify({
        "mensagem": "Servidor funcionando",
        "total_produtos": total_produtos,
        "total_pedidos": total_pedidos
    }), 200

@app.route("/estoque", methods=["GET"])
def consultar_estoque():
    with lock_banco:
        resultado = []
        for nome, dados in banco["produtos"].items():
            resultado.append({
                "codigo": dados["codigo"],
                "nome": nome,
                "quantidade": dados["quantidade"]
            })

    return jsonify(resultado), 200

# retorna os pedidos feitos
@app.route("/pedidos", methods=["GET"])
def listar_pedidos():
    with lock_banco:
        resultado = []
        for pedido in banco["pedidos"]:
            resultado.append({
                "pedido_id": pedido["id"],
                "produto": pedido["produto"],
                "quantidade_comprada": pedido["quantidade"]
            })

    return jsonify(resultado), 200

@app.route("/comprar", methods=["POST"])
def comprar():
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "JSON não enviado."}), 400

    produto = str(dados.get("produto", "")).strip().lower()
    qtd = dados.get("quantidade")

    if not produto or qtd is None:
        return jsonify({"erro": "Os campos 'produto' e 'quantidade' são obrigatórios."}), 400

    if qtd <= 0:
        return jsonify({"erro": "Quantidade inválida."}), 400

    with lock_banco:
        item = banco["produtos"].get(produto)

        if item is None:
            return jsonify({"erro": "Produto não encontrado."}), 404

        if item["quantidade"] < qtd:
            return jsonify({"erro": "Estoque insuficiente."}), 400

        item["quantidade"] -= qtd

        pedido = {
            "id": banco["proximo_pedido_id"],
            "produto": produto,
            "quantidade": qtd
        }

        banco["pedidos"].append(pedido)
        banco["proximo_pedido_id"] += 1

        estoque_restante = item["quantidade"]

    return jsonify({
        "mensagem": "Pedido realizado com sucesso!",
        "produto": produto,
        "quantidade_comprada": qtd,
        "estoque_restante": estoque_restante
    }), 200

if __name__ == "__main__":
    app.run(threaded=True)