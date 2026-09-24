def cadastroUsuario (nome,email,senha,confirmarSenha):
    if nome == "":
        return "Nome Obrigatorio"
    if email =="":
        return "Email Obrigatorio"
    if "@" not in email:
        return "Email Inválido"
    if senha =="":
        return "Senha Obrigatoria"
    if len(senha) < 6:
        return "A senha deve possuir pelo menos 6 caracteres"
    if senha != confirmarSenha:
        return "As senhas não coincidem"

##verificar email no banco

##enviar para o banco
    return "Usuario cadastrado com sucesso"
    
def loginUsuario (email,senha):
    if email == "":
        return "Email Obrigatorio"
    if "@" not in email:
        return "Email Invalido"
    if senha == "":
        return "Senha Obrigatoria"

#verificar email e senha no banco

def alterarUsuario (email,novoNome,novoEmail,novaSenha):
    if email == "":
        return "Email Obrigatorio"
    if novoNome == "":
        return "Nome obrigatorio"
    if novoEmail == "":
        return "Email Obrigatorio"
    if "@" not in novoEmail:
        return "Email Invalido"
    if novaSenha == "":
        return "Senha obrigatoria"
    if len(novaSenha) < 6:
        return "Senha Invalida"
        
##buscar usuario pelo Email
##atualizar dados no banco


def excluirUsuario (email):
    if email == "":
        return "Email Obrigatorio"
    if "@" not in email:
        return "Email Invalido"
    
#exluir usuario do banco de dados