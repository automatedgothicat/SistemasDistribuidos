from flask import Flask, request, jsonify

app = Flask(__name__)

# lista de disciplinas com número de vagas
disciplinas = {
    "EC00AED1":{"nome":"Algoritmos e Estruturas de Dados I",
                "vagas":40, "matriculados":[]},
    "EC00AED2":{"nome":"Algoritmos e Estruturas de Dados II",
                "vagas":40, "matriculados":[]},
    "EC00AED3":{"nome":"Algoritmos e Estruturas de Dados III",
                "vagas":40, "matriculados":[]},
    "EC0000SD":{"nome":"Sistemas Distribuídos",
                "vagas":30, "matriculados":[]}
} # defina aqui as disciplinas

# URL que deve acionar a função
@app.route("/")
def tela_inicial():
    return "<p> BEM VINDO AO SD ACADÊMICO </p>"

@app.route("/status", methods={"GET"})
def verifica_status():
    return jsonify(" -- Servidor em funcionamento -- ")

@app.route("/disciplinas", methods=["GET"])
def lista_disciplinas():
    saida = {}

    for codigo, dados in disciplinas.items():
        saida[codigo] = {
            "Disciplina": dados["nome"],
            "Vagas": dados["vagas"]
        }
    return jsonify(saida)

@app.route("/matriculas/<codigo>",methods=["GET"])
def matriculados(codigo):
    if codigo in disciplinas:
        info = disciplinas[codigo]

        return jsonify({
            "codigo": codigo,
            "disciplina": info["nome"],
            "vagas": info["vagas"],
            "matriculados": info["matriculados"]
        })
    return jsonify({"erro": "Código de disciplina informado não encontrado!"}), 404

@app.route("/matricula",methods=["POST"])
def matricula():
    dados = request.get_json()

    disciplina = dados.get("disciplina", "").strip()
    nome_aluno = dados.get("nome", "").strip()

    ''' Adicionar um for para percorrer a variável "disciplinas"
        no qual verifique se existe a disciplina que o aluno
        informou no lado do cliente
        Verificar se o aluno já não está adicionado na disciplina
        Verificar se existe vagas para a a disciplina que permitam
        fazer a matricula do aluno
    '''

    return jsonify({"erro": "Disciplina não encontrada"}), 404   

# rodando o servidor Flask
if __name__ == "__main__":
    app.run()