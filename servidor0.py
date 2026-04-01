# python -m venv .sistdist
# ...\.sistdist\Scripts\Activate.bat
# ...\.sistdist\Scripts\python.exe -m pip install flask requests

from flask import Flask, request, jsonify
import time
import random

app = Flask(__name__) # criando a aplicação Flask 

# Dados em memória referente ao estoque
estoque = {"camiseta": 10}

pedidos = [] # cada item temos chave:valor
proximo_id = 1

# Retorna com a informação de servidor funcionando e quantos pedidos possui.
@app.route("/status", methods=["GET"]) # app.route: ligar uma URL (rota) a uma função do Flask
def status():
    return jsonify({
        "mensagem": "Servidor funcionando",
        "total_pedidos": len(pedidos)
    })

# retorna o estoque atual
@app.route("/estoque", methods=["GET"])
def consultar_estoque():
    return jsonify(estoque)

# retorna os pedidos feitos
@app.route("/pedidos", methods=["GET"])
def listar_pedidos():
    return jsonify(pedidos)

# registra uma compra
@app.route("/comprar", methods=["POST"])
def comprar():
    global proximo_id

    dados = request.get_json()

    produto = dados.get("produto")
    quantidade = dados.get("quantidade", 1)
    simular_atraso = dados.get("simular_atraso", False) # se True, espera entre 5 e 10 segundos

    if produto not in estoque:
        return jsonify({"erro": "Produto não encontrado"}), 404 # 404: rota solicitada não encontrada

    if quantidade <= 0:
        return jsonify({"erro": "Quantidade inválida"}), 400 # 400: servidor não processa a requisição do cliente

    if estoque[produto] < quantidade:
        return jsonify({"erro": "Estoque insuficiente"}), 400

    # Simula lentidão do servidor/rede
    if simular_atraso:
        atraso = random.randint(5, 10)
        print(f"[SERVIDOR] Simulando atraso de {atraso} segundos...")
        time.sleep(atraso)

    # Registra a compra
    estoque[produto] -= quantidade

    pedido = {
        "id": proximo_id,
        "produto": produto,
        "quantidade": quantidade
    }

    pedidos.append(pedido)
    proximo_id += 1

    return jsonify({
        "mensagem": "Compra realizada com sucesso",
        "pedido": pedido,
        "estoque_atual": estoque[produto]
    })

# rodando o servidor Flask
if __name__ == "__main__":
    # flask --app app run
    app.run() # rodando servidor localmente

