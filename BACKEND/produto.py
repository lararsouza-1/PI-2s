def cadastrarProduto(nome, preco, quantidade):
    if nome == "":
        return "Nome obrigatorio"

    if preco <= 0:
        return "O preço deve ser maior que zero"

    if not isinstance(quantidade, int):
        return "A quantidade deve ser um número inteiro"

    if quantidade <= 0:
        return "A quantidade deve ser maior que zero"

    # cadastrar produto no banco}

def buscarProduto(id=None, nome=None):
       if id is None and nome is None:
            return "Informe o ID ou o nome do produto"

       if id is not None and not isinstance(id, int):
        return "O ID deve ser um número inteiro"

       if id is not None and id <= 0:
            return "ID invalido"

       if id is None and nome == "":
            return "Nome invalido"
            