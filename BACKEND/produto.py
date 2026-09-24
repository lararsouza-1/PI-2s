def cadastrarProduto (nome,preco,quantidade):
    if nome == "":
        return "Nome obrigatorio"
    if preco <= 0:
        return "O preço deve ser maior que zero"
    if not isinstance(quantidade, int):
    if quantidade <=0:
        return "A quantidade deve ser maior que zero"

#cadastrar produto no banco