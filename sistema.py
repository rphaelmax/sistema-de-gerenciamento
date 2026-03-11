# Conter as informações dos produtos em um dicionário
estoque = {
    "produto": {
        "nome": "teste",
        "custo de produção": 50.00,
        "preço de venda": 100.00,
        "quantidade em estoque": 3
    }
}

# Buscar produto:
def buscar_produto(nome):
    nome = nome.strip().lower()

    # busca pela chave diretamente
    if nome in estoque:
        return nome

    # busca pelo campo 'nome' dentro do dicionário
    for chave, info in estoque.items():
        if info['nome'].lower() == nome:
            return chave
    return None

# Exibir o estoque:
def menu_exibir_estoque():
    print("\nEstoque atual:")
    if not estoque:
        print("Estoque vazio!")
        return
    for nome, info in estoque.items():
        print(f"Produto: {info['nome']}, Custo de Produção: R${info['custo de produção']:.2f}, Preço de Venda: R${info['preço de venda']:.2f}, Quantidade em Estoque: {info['quantidade em estoque']}")

# Cadastro de produto:
def menu_cadastrar_produto():
    nome = input("Insira o nome do produto: ").strip().lower()

    if nome in estoque:
        print("Produto já cadastrado.")
        return

    custo = float(input("Insira o custo de produção: R$").strip())
    preco = float(input("Insira o preço de venda: R$").strip())
    quantidade = int(input("Insira a quantidade inicial em estoque: ").strip())

    estoque[nome] = {
        "nome": nome,
        "custo de produção": custo,
        "preço de venda": preco,
        "quantidade em estoque": quantidade
    }
    print(f"Produto '{nome}' cadastrado com sucesso!")

# Registro de produção
def menu_registrar_producao():
    nome = input("Insira o nome do produto: ").strip()
    chave = buscar_produto(nome)

    if chave:
        print(f"Quantidade atual em estoque: {estoque[chave]['quantidade em estoque']}")
        quantidade = int(input("Insira a quantidade produzida: ").strip())
        estoque[chave]["quantidade em estoque"] += quantidade
        print(f"\n{quantidade} unidades de '{nome}' adicionadas ao estoque.")
    else:
        print("Produto não encontrado.")

# Venda:
# Quando vender: reduz estoque; soma faturamento; não pode vender sem estoque
def menu_vender_produto():
    nome = input("Insira nome do produto: ").strip()
    chave = buscar_produto(nome)
    
    if chave:
        print(f"Quantidade em estoque disponível: {estoque[chave]['quantidade em estoque']}")
        quantidade = input("Insira quantidade a vender: ").strip()
        vender_produto(chave, quantidade)
    else:
        print("Produto não encontrado.")

def vender_produto(nome_produto, quantidade_vendida):
    quantidade_vendida = int(quantidade_vendida)

    if nome_produto in estoque:
        produto = estoque[nome_produto]

        if produto["quantidade em estoque"] >= quantidade_vendida:
            produto["quantidade em estoque"] -= quantidade_vendida
            faturamento = produto["preço de venda"] * quantidade_vendida
            print(f"\nVendido {quantidade_vendida} unidades de {produto['nome']}. Faturamento: R${faturamento:.2f}")

            if produto["quantidade em estoque"] == 0:
                estoque.pop(nome_produto)
                print(f"\nEstoque de '{nome_produto}' zerado, produto removido do estoque.")
        else:
            print(f"\nEstoque insuficiente para vender {quantidade_vendida} unidades de {produto['nome']}.")

# Por trás das funções:
# A ideia de utilizar um dicionário de funções automatizado/filtrado surgiu da necessidade de evitar a criação manual de cada entrada no dicionário, priorizando praticidade
# Foi utilizado a ajuda de IA para implementar essa lógica na prática

# O programa usa globals(), que é uma função que mostra tudo que existe no programa naquele momento
# A partir disso, o código filtra apenas funções que podem ser executadas
# Ele verifica: se o objeto pode ser chamado (callable); se é realmente uma função criada no código (__code__); e se ela vem das células executadas no ambiente do notebook


# As funções que devem aparecer somente no menu começam com 'menu_'
# Esse prefixo serve apenas para separar as funções que o usuário/cliente pode usar das funções internas do programa
funcoes = {
    nome.replace('menu_', ''): obj
    for nome, obj in globals().items()
    if callable(obj)
    and hasattr(obj, '__code__')
    # Acho o python já identifica o que é código criado no programa, então não precisa do filtro de filename, mas se for um ambiente de notebook, ele pode acabar pegando funções criadas durante a execução do programa, por isso o filtro de filename
    # and (obj.__code__.co_filename.startswith('/tmp/ipykernel') or obj.__code__.co_filename.startswith('<ipython-input') or 'ipykernel' in obj.__code__.co_filename) # aqui filtra no vscode, colab e jupyter notebook (eu acho, dependendo do ambiente possa ter que ajustar)
    and nome.startswith('menu_')
}
opcoes = list(funcoes.keys()) # Cria antes do menu começar a rodar pra evitar que novas variáveis criadas durante o programa acabem aparecendo por acidente

# Rodar o programa infinitas vezes até o usuário digitar sair
while True:
    print("\n***** Funções disponíveis: *****")
    for i, nome in enumerate(opcoes):  # Percorre a lista de funções disponíveis para montar o menu numerado exibido ao usuário
        print(f"  {i+1}. {nome.replace('_', ' ')}")

    comando = input("\nInsira o número da função ou digite sair: ").strip().lower()

    if comando == "sair":
        print("\nTerminando tarefa!")
        break
    elif comando.isdigit() and 1 <= int(comando) <= len(opcoes):  # Valida se a entrada é um número e se corresponde a uma opção existente no menu
        funcao = funcoes[opcoes[int(comando) - 1]]  # Pega a função correspondente à opção escolhida pelo usuário

        # Analisa a função para descobrir automaticamente quantos argumentos ela precisa e quais são seus nomes
        # Foi utilizado a ajuda de IA
        num_args = funcao.__code__.co_argcount
        args_necessarios = funcao.__code__.co_varnames[:num_args]

        args_coletados = []
        for arg in args_necessarios:
            valor = input(f"Insira {arg.replace('_', ' ')}: ").strip()
            args_coletados.append(valor)
        
        funcao(*args_coletados)  # O * desempacota a lista args_coletados, fazendo com que cada valor dentro dela seja passado separadamente como argumento para a função
    else:
        print("\nOpção inválida.")