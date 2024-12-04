import random  # Para gerar números aleatórios nos primos do RSA
import math    # Para cálculos matemáticos


# Funções para Criptografia Simétrica

# Função para criptografar usando método XOR
def des_criptografar(mensagem, chave):
    chave = chave[:8]  # Garantimos que a chave tenha no máximo 8 caracteres
    mensagem_cifrada = ""
    for i in range(len(mensagem)):
        # Realiza XOR entre cada caractere da mensagem e da chave
        mensagem_cifrada += chr(ord(mensagem[i]) ^ ord(chave[i % len(chave)]))
    return mensagem_cifrada

# Função para descriptografar usando método XOR (simula DES)
def des_descriptografar(mensagem_cifrada, chave):
    # A descriptografia é o mesmo processo da criptografia com XOR
    return des_criptografar(mensagem_cifrada, chave)


# Funções para Criptografia RSA

# Função para verificar se um número é primo
# se o numero for menor que dois e o resto da divisão dele for 0 ele nao é considerado um numero primo e essa função vai rodar ate um numero primo ser encontrado.
def primo(n):
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

# Função para gerar chaves RSA
def gerar_chaves_rsa(tamanho_primo=16):
    p = random.randint(2**(tamanho_primo - 1), 2**tamanho_primo - 1) 
    while not primo(p):
        p = random.randint(2**(tamanho_primo - 1), 2**tamanho_primo - 1)
    q = random.randint(2**(tamanho_primo - 1), 2**tamanho_primo - 1)
    while not primo(q) or q == p:
        q = random.randint(2**(tamanho_primo - 1), 2**tamanho_primo - 1)
    # 1- Geramos os numeros primos com uma semente aleatoria dentro de um intervalo com a funcão randing e o intervalo é dado a partir da operação matematica com esponeciaçao e subtração 
    # 2- fazemos a verificação com o while not pra descobrir se realmente é um numero primo com a função de verificação de numero primo
    # 3- Pra verificar se q não é igual a p verificamos isso também no segundo while not pq não podemos usar o mesmo número primo duas vezes no RSA
    
    n = p * q  # Calcula n multiplicando dois numeros primos 
    phi = (p - 1) * (q - 1)  # Calcula phi usando os numeros primos 
    e = 65537  # Valor comum para o expoente público
    while math.gcd(e, phi) != 1:  # Garante que e seja coprimo com phi se caso nao for ele adiciona +2 em e
        e += 2
    d = pow(e, -1, phi)  # Calcula o inverso modular de e em relação a phi
    return (e, n), (d), (p, q)

# Função para criptografar uma mensagem usando RSA
def rsa_criptografar(mensagem, chave_publica):
    e, n = chave_publica
    mensagem_cifrada = [pow(ord(c), e, n) for c in mensagem]
    mensagem_cifrada_str = " ".join(map(str, mensagem_cifrada))
    return f"Lista de números criptografados:\n{mensagem_cifrada}\n\nMensagem cifrada apenas com espaco:\n{mensagem_cifrada_str}\n"

# Função para descriptografar uma mensagem usando RSA
def rsa_descriptografar(mensagem_cifrada, chave_privada):
    d, n = chave_privada
    mensagem_original = ''.join([chr(pow(c, d, n)) for c in mensagem_cifrada])
    return mensagem_original

# ========================
# Interface do Usuário
# ========================

# Função para exibir o menu principal
def menu():
    print("\n=== Sistema de Criptografia ===\n")
    print("\n1. Criptografia Simétrica")
    print("\n2. Criptografia Assimétrica")
    print("\n3. Sair")
    return input("\nEscolha uma opção: ")

# Função para executar operações com DES
def executar_des():
    opcao = input("Deseja: \n1-Criptografar\n2-Descriptografar ")
    texto = input("\nDigite o texto(sem espaço): ")
    chave = input("\nDigite a chave (máximo 8 caracteres): ")
    if opcao == "1":
        resultado = des_criptografar(texto, chave)
        print(f"Texto Criptografado: {resultado}")
    elif opcao == "2":
        resultado = des_descriptografar(texto, chave)
        print(f"Texto Descriptografado: {resultado}")

# Função para executar operações com RSA
def executar_rsa():
    print("1. Gerar Chaves RSA")
    print("2. Criptografar Mensagem")
    print("3. Descriptografar Mensagem")
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        chave_publica, chave_privada, primos = gerar_chaves_rsa()
        print(f"Chave Pública (e, n): {chave_publica}")
        print(f"Chave Privada (d, n): {chave_privada}")
        print(f"Primos usados (p, q): {primos}")
    elif opcao == "2":
        e = int(input("Digite o valor de e: "))
        n = int(input("Digite o valor de n: "))
        mensagem = input("Digite a mensagem: ")
        resultado = rsa_criptografar(mensagem, (e, n))
        print(f"Mensagem Criptografada: {resultado}")
    elif opcao == "3":
        d = int(input("Digite o valor de d: "))
        n = int(input("Digite o valor de n: "))
        mensagem_cifrada = input("Digite a mensagem cifrada (números separados por espaço): ")
        mensagem_cifrada = [int(x) for x in mensagem_cifrada.split()]
        resultado = rsa_descriptografar(mensagem_cifrada, (d, n))
        print(f"Mensagem Descriptografada: {resultado}")

# ========================
# Execução do Programa
# ========================

# Loop principal
while True:
    escolha = menu()
    if escolha == "1":
        executar_des()
    elif escolha == "2":
        executar_rsa()
    elif escolha == "3":
        print("Encerrando...")
        break
    else:
        print("Opção inválida, tente novamente.")
