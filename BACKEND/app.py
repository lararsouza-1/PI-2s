from flask import Flask,  jsonify, request

from produto import listarProdutos, cadastrarProduto

app = Flask(__name__)

@app.route("/")
def inicio():
    return "Bem vindo ao sistema Anvellis"


@app.route("/produtos")
def produtos():
    lista = listarProdutos()
    resultado = []

    for produto in lista:
        dados = {
            "id": produto[0],
            "nome": produto[1],
            "preco": produto[2],
            "quantidade": produto[3]
        }

        resultado.append(dados)
    
    return jsonify(resultado)

@app.route("/produtos", methods=["POST"])
def cadastrar():
    dados = request.get_json(silent=True)

    if not isinstance(dados, dict):
        return jsonify({"mensagem": "Envie um objeto JSON válido"}), 400
    
    nome = dados.get("nome")
    preco = dados.get("preco")
    quantidade = dados.get("quantidade")

    mensagem = cadastrarProduto(nome,preco,quantidade)

    if mensagem == "Produto cadastrado com sucesso!":
        return jsonify({"mensagem": mensagem}), 201
    else:
        return jsonify({"mensagem": mensagem}), 400

    
if __name__ == "__main__":
    app.run(debug=True)