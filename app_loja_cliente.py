import requests

BASE_URL = "http://127.0.0.1:5000" #endereço base do servidor http://127.0.0.1:5000/

def ver_status():
    resposta = requests.get(f"{BASE_URL}/status")
    print("\nSTATUS DO SERVIDOR")
    print(resposta.json())

def ver_estoque():
    resposta = requests.get(f"{BASE_URL}/estoque")
    print("\nESTOQUE")
    print(resposta.json())

def ver_pedidos():
    resposta = requests.get(f"{BASE_URL}/pedidos")
    print("\nPEDIDOS")
    print(resposta.json())

def comprar(produto, quantidade):
    dados = {
        "produto": produto,
        "quantidade": quantidade
    }

    resposta = requests.post(f"{BASE_URL}/comprar",json=dados)

    print("\nRESPOSTA DA COMPRA")
    print(resposta.status_code, resposta.json())
    
if __name__ == "__main__":
    ver_status()
    ver_estoque()

    print("\n--- COMPRA NORMAL ---")
    item = input("Informe o item: ")
    q_item = input("Quantidade do item: ")
    comprar(item, int(q_item))
    ver_estoque()
    ver_pedidos()