import requests

BASE_URL = "http://127.0.0.1:5000"

def status_server():
    saida = requests.get(f"{BASE_URL}/status")
    print("\nStatus do servidor")
    print(saida.json())

def listar_disciplinas():
    saida = requests.get(f"{BASE_URL}/disciplinas")
    print("\nDISCIPLINAS")
    print(saida.json())

def matriculados_disciplina(codigo):
    saida = requests.get(f"{BASE_URL}/matriculas/{codigo}")
    print("\nALUNOS MATRICULADOS")
    print(saida.json())

def matricula(disciplina, nome_aluno):
    dados = {
        "disciplina": disciplina,
        "nome": nome_aluno
    }

    saida = requests.post(f"{BASE_URL}/matricula", json=dados)
    print(saida.status_code, saida.json())

if __name__ == "__main__":
    status_server()
    listar_disciplinas()
    matricula("Sistemas Distribuídos","Ciclano Souza")
    matricula("Sistemas Distribuídos","Fulano da Silva")
    matricula("Sistemas Distribuídos","Beltrano Alves")
    listar_disciplinas()
    matriculados_disciplina("SD")