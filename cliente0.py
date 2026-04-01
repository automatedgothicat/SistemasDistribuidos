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


def comprar(produto, quantidade, simular_atraso=False, timeout=None):
    dados = {
        "produto": produto,
        "quantidade": quantidade,
        "simular_atraso": simular_atraso
    }

    try:
        resposta = requests.post(
            f"{BASE_URL}/comprar",
            json=dados,
            timeout=timeout
        )
        print("\nRESPOSTA DA COMPRA")
        print(resposta.status_code, resposta.json())
    except requests.exceptions.Timeout:
        print("\nO cliente desistiu de esperar: TIMEOUT")
    except requests.exceptions.ConnectionError:
        print("\nNão foi possível conectar ao servidor.")


if __name__ == "__main__":
    ver_status()
    ver_estoque()

    print("\n--- COMPRA NORMAL ---")
    comprar("camiseta", 1)

    ver_estoque()
    ver_pedidos()