import os
import pandas as pd


# Função para limpar o terminal
def limpar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


# Obter o caminho absoluto para a área de trabalho
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

# Definir os caminhos completos para os arquivos
usuarios_file = os.path.join(desktop_path, "usuarios.txt")
vendas_file = os.path.join(desktop_path, "vendas.txt")
estoque_file = os.path.join(desktop_path, "estoque.txt")

# Verificar e criar os arquivos se não existir
for file_path in [usuarios_file, vendas_file, estoque_file]:
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            pass


# Função de login
def login():
    limpar_terminal()
    print("==== Login ====")
    username = input("Digite seu nome de usuário: ")
    password = input("Digite sua senha: ")

    # Verificar se o usuário e senha estão corretos
    with open(usuarios_file, 'r') as file:
        for line in file:
            stored_username, stored_password = line.strip().split(',')
            if username == stored_username and password == stored_password:
                limpar_terminal()
                return True

    limpar_terminal()
    print("Usuário não encontrado.")

    criar_novo_usuario = input("Deseja criar uma nova conta? (s/n): ")
    if criar_novo_usuario.lower() == "s":
        novo_username = input("Digite o novo nome de usuário: ")
        novo_password = input("Digite a nova senha: ")

        # Salvar os detalhes do novo usuário no arquivo de texto
        with open(usuarios_file, 'a') as file:
            file.write(f"{novo_username},{novo_password}\n")

        limpar_terminal()
        print("Nova conta criada. Faça login novamente.")
        input("Pressione Enter para continuar...")
        return False
    else:
        limpar_terminal()
        print("Operação cancelada.")

    return False


# Função para registrar uma venda
def registrar_venda():
    limpar_terminal()
    print("==== Registrar Venda ====")
    produto = input("Digite o nome do produto: ")
    quantidade = int(input("Digite a quantidade vendida: "))
    preco_unitario = float(input("Digite o preço unitário: "))

    # Verificar se o produto está no estoque e se a quantidade é suficiente
    estoque = carregar_estoque()
    if produto not in estoque:
        print("Erro: Produto não encontrado no estoque.")
        return

    estoque_atual = estoque[produto]
    if quantidade > estoque_atual:
        print("Erro: Quantidade insuficiente em estoque.")
        return

    total = quantidade * preco_unitario

    # Salvar os detalhes da venda no arquivo de texto
    with open(vendas_file, 'a') as file:
        file.write(f"{produto},{quantidade},{preco_unitario},{total}\n")

    # Atualizar o estoque
    estoque[produto] -= quantidade
    salvar_estoque(estoque)

    print("Venda registrada com sucesso!")


# Função para registrar um produto em estoque
def registrar_produto():
    limpar_terminal()
    print("==== Registrar Produto em Estoque ====")
    # Obter os detalhes do produto
    produto = input("Digite o nome do produto: ")
    quantidade = int(input("Digite a quantidade em estoque: "))

    # Salvar os detalhes do produto no arquivo de texto
    with open(estoque_file, 'a') as file:
        file.write(f"{produto},{quantidade}\n")

    print("Produto registrado com sucesso!")


# Função para excluir um produto do estoque
def excluir_produto():
    limpar_terminal()
    print("==== Excluir Produto do Estoque ====")
    produto = input("Digite o nome do produto que deseja excluir: ")

    estoque = carregar_estoque()
    if produto not in estoque:
        print("Erro: Produto não encontrado no estoque.")
        return

    del estoque[produto]
    salvar_estoque(estoque)

    print("Produto excluído com sucesso!")


# Função para alterar um produto do estoque
def alterar_produto():
    limpar_terminal()
    print("==== Alterar Produto do Estoque ====")
    produto = input("Digite o nome do produto que deseja alterar: ")

    estoque = carregar_estoque()
    if produto not in estoque:
        print("Erro: Produto não encontrado no estoque.")
        return

    quantidade = int(input("Digite a nova quantidade em estoque: "))
    estoque[produto] = quantidade
    salvar_estoque(estoque)

    print("Produto alterado com sucesso!")


# Função para alterar a senha de um usuário existente
def alterar_senha():
    limpar_terminal()
    print("==== Alterar Senha ====")
    username = input("Digite seu nome de usuário: ")
    password = input("Digite sua senha atual: ")

    # Verificar se o usuário e senha estão corretos
    with open(usuarios_file, 'r') as file:
        lines = file.readlines()

    found = False
    for i, line in enumerate(lines):
        stored_username, stored_password = line.strip().split(',')
        if username == stored_username and password == stored_password:
            found = True
            break

    if not found:
        print("Erro: Usuário não encontrado ou senha incorreta.")
        return

    new_password = input("Digite a nova senha: ")
    lines[i] = f"{username},{new_password}\n"

    with open(usuarios_file, 'w') as file:
        file.writelines(lines)

    print("Senha alterada com sucesso!")


# Função para carregar o estoque em um dicionário
def carregar_estoque():
    estoque = {}

    if os.path.exists(estoque_file):
        with open(estoque_file, 'r') as file:
            for line in file:
                produto, quantidade = line.strip().split(',')
                estoque[produto] = int(quantidade)

    return estoque


# Função para salvar o estoque de volta no arquivo
def salvar_estoque(estoque):
    with open(estoque_file, 'w') as file:
        for produto, quantidade in estoque.items():
            file.write(f"{produto},{quantidade}\n")


# Função para extrair todos os relatórios
def extrair_relatorios():
    limpar_terminal()
    print("==== Extrair Relatórios ====")

    # Verificar se o arquivo de usuários existe
    if os.path.exists(usuarios_file):
        gerar_relatorio(usuarios_file)
    else:
        print("O arquivo de usuários não existe.")

    # Verificar se o arquivo de vendas existe
    if os.path.exists(vendas_file):
        gerar_relatorio(vendas_file)
    else:
        print("O arquivo de vendas não existe.")

    # Verificar se o arquivo de estoque existe
    if os.path.exists(estoque_file):
        gerar_relatorio(estoque_file)
    else:
        print("O arquivo de estoque não existe.")


# Função que gera os relatórios
def gerar_relatorio(arquivo):
    if not os.path.exists(arquivo):
        print(f"O arquivo '{arquivo}' não existe.")
        return

    # Ler o arquivo e criar uma lista com os valores
    data = []
    with open(arquivo, 'r') as file:
        for line in file:
            data.append(line.strip().split(','))

    # Criar um DataFrame com os dados
    df = pd.DataFrame(data)

    # Obter o número de colunas
    num_colunas = len(df.columns)

    # Gerar nomes de colunas padrão (Coluna1, Coluna2, ...)
    colunas = [f"Coluna{i}" for i in range(1, num_colunas + 1)]

    # Definir os nomes das colunas no DataFrame
    df.columns = colunas

    # Exibir o DataFrame
    print(df)


# Loop principal do programa
def main():
    if not login():
        return

    input('''
    ██████╗ ███████╗███╗   ███╗    ██╗   ██╗██╗███╗   ██╗██████╗  ██████╗ 
    ██╔══██╗██╔════╝████╗ ████║    ██║   ██║██║████╗  ██║██╔══██╗██╔═══██╗
    ██████╔╝█████╗  ██╔████╔██║    ██║   ██║██║██╔██╗ ██║██║  ██║██║   ██║
    ██╔══██╗██╔══╝  ██║╚██╔╝██║    ╚██╗ ██╔╝██║██║╚██╗██║██║  ██║██║   ██║
    ██████╔╝███████╗██║ ╚═╝ ██║     ╚████╔╝ ██║██║ ╚████║██████╔╝╚██████╔╝
    ╚═════╝ ╚══════╝╚═╝     ╚═╝      ╚═══╝  ╚═╝╚═╝  ╚═══╝╚═════╝  ╚═════╝
                           _____         __  __ ______ 
                          / ____|  /\   |  \/  |  ____|
                         | (___   /  \  | \  / | |__   
                          \___ \ / /\ \ | |\/| |  __|  
                          ____) / ____ \| |  | | |____ 
                         |_____/_/    \_\_|  |_|______|


                             PRESSIONE ENTER


    ''')

    while True:
        limpar_terminal()
        print("==== Sistema de Gerenciamento de Estoque ====")
        print("Selecione uma opção:")
        print("1. Registrar Produto em Estoque")
        print("2. Excluir Produto do Estoque")
        print("3. Alterar Produto do Estoque")
        print("4. Registrar Venda")
        print("5. Alterar Senha")
        print("6. Extrair Relatórios")
        print("7. Sair")

        opcao = input("Digite o número da opção desejada: ")

        if opcao == "1":
            registrar_produto()
        elif opcao == "2":
            excluir_produto()
        elif opcao == "3":
            alterar_produto()
        elif opcao == "4":
            registrar_venda()
        elif opcao == "5":
            alterar_senha()
        elif opcao == "6":
            extrair_relatorios()
        elif opcao == "7":
            limpar_terminal()
            print("Obrigado por usar o Sistema de Gerenciamento de Estoque!")
            break
        else:
            print("Opção inválida. Digite novamente.")

        input("Pressione Enter para continuar...")


if __name__ == '__main__':
    main()
