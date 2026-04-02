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
    # listar_disciplinas()
    # matricula("Sistemas Distribuídos","Ciclano Souza")
    # matricula("Sistemas Distribuídos","Fulano da Silva")
    # matricula("Sistemas Distribuídos","Beltrano Alves")
    # listar_disciplinas()
    # matriculados_disciplina("SD")

    ans = 0
    while ans != 0:
        print('''
              0 - Fechar/sair
              1 - Listar disciplinas
              2 - Listar matriculados em uma disciplina
              3 - Matricular em uma disciplina
        ''')
        ans = input("Insira o número da ação desejada:")

        if ans == "1":
            listar_disciplinas()
        elif ans == "2":
            codigo = input("Insira o código da disciplina:")
            matriculados_disciplina(codigo)
        elif ans == "3":
            nome_disciplina = input("Insira o nome da disciplina:")
            nome_aluno = input("Insira o nome do aluno:")
            matricula(nome_disciplina,nome_aluno)
            print("Cadastrando ", nome_aluno, " em ", nome_disciplina)
        else:
            print("Tente novamente")
    print("Programa encerrado")
